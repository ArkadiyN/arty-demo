#!/usr/bin/env python3
import os
import json
import glob
import sys

# Define the root projects path as a constant
PROJECTS_ROOT = os.path.expanduser("~/.claude/projects")

def find_expensive_calls(project_name, session_id):
    entries = []
    
    # 1. Build paths to the specific files requested
    project_dir = os.path.join(PROJECTS_ROOT, project_name)
    main_session_file = os.path.join(project_dir, f"{session_id}.jsonl")
    subagents_glob = os.path.join(project_dir, session_id, "subagents", "*.jsonl")
    
    files_to_parse = []
    if os.path.exists(main_session_file):
        files_to_parse.append((main_session_file, "Main"))
    else:
        print(f"⚠️  Main session file not found: {main_session_file}")
        
    for sub_file in glob.glob(subagents_glob):
        files_to_parse.append((sub_file, "Subagent"))

    if not files_to_parse:
        print(f"❌ No log files found for project '{project_name}' and session '{session_id}'.")
        return

    # 2. Parse target files
    for file_path, source_type in files_to_parse:
        file_base = os.path.splitext(os.path.basename(file_path))[0]
        id_suffix = f"..{file_base[-6:]}" if len(file_base) >= 6 else file_base
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    
                    message_obj = data.get("message")
                    if not isinstance(message_obj, dict):
                        continue
                        
                    usage = message_obj.get("usage")
                    if not usage or "output_tokens" not in usage:
                        continue
                    
                    out_tokens = usage["output_tokens"]
                    in_tokens = usage.get("input_tokens", 0)
                    cache_read = usage.get("cache_read_input_tokens", 0)
                    
                    # Track tool call info vs raw text conversational steps
                    detected_tool = "Text Message"
                    content_preview = "Unknown Content"
                    
                    content_list = message_obj.get("content", [])
                    if isinstance(content_list, list):
                        for item in content_list:
                            if not isinstance(item, dict):
                                continue
                                
                            # Extract Tool Executions
                            if item.get("type") == "tool_use":
                                tool_name = item.get("name", "UnknownTool")
                                tool_input = item.get("input", {})
                                filename = os.path.basename(tool_input.get("file_path", "unknown_file"))
                                
                                # Assign the tool name column data
                                detected_tool = tool_name
                                
                                # Make the preview concise based on the tool signature
                                if tool_name == "str_replace_editor" or tool_input.get("command") == "str_replace":
                                    old_snippet = tool_input.get("old_str", "")[:15].strip().replace('\n', ' ')
                                    new_snippet = tool_input.get("new_str", "")[:15].strip().replace('\n', ' ')
                                    content_preview = f"[{filename}] Replace: '{old_snippet}' -> '{new_snippet}'"
                                elif "file_path" in tool_input:
                                    content_preview = f"Target File: {filename}"
                                else:
                                    content_preview = f"Arguments: {list(tool_input.keys())}"
                                    
                            # Extract Standard Text Conversational Steps (Fallback)
                            elif item.get("type") == "text" and content_preview == "Unknown Content":
                                content_preview = item.get("text", "").strip()

                    entries.append({
                        "id_suffix": id_suffix,
                        "source_type": source_type,
                        "line": line_num,
                        "output_tokens": out_tokens,
                        "input_tokens": in_tokens,
                        "cache_read": cache_read,
                        "tool_name": detected_tool,
                        "preview": content_preview
                    })
                    
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

    # 3. Sort and print the leaderboard
    entries.sort(key=lambda x: x['output_tokens'], reverse=True)

    print(f"\n{'='*52} SESSION LEADERBOARD {'='*53}")
    print(f"{'RANK':<5} | {'OUT TOKENS':<11} | {'IN TOKENS':<11} | {'CACHE READ':<11} | {'ID (6 CHARS)':<14} | {'TOOL COLUMN':<20} | {'MESSAGE PREVIEW'}")
    print("-" * 126)
    
    for i, entry in enumerate(entries[:15], 1):
        preview = str(entry['preview'])
        preview_clipped = preview[:42] + '...' if len(preview) > 42 else preview
        preview_clipped = preview_clipped.replace('\n', ' ')
        
        type_label = "Main" if entry['source_type'] == "Main" else "Sub"
        origin_id = f"{type_label} ({entry['id_suffix']})"
        
        print(f"{i:<5} | {entry['output_tokens']:<11,} | {entry['input_tokens']:<11,} | {entry['cache_read']:<11,} | {origin_id:<14} | {entry['tool_name']:<20} | {preview_clipped}")
    print(f"{'='*126}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 analyze_tokens.py <project_name> <session_id>")
        print("Example: python3 analyze_tokens.py my-git-repo 600a83e8-0b3d-4138-aeba-20bb4f759ee2")
        sys.exit(1)
        
    sys_project = sys.argv[1]
    sys_session = sys.argv[2]
    
    find_expensive_calls(sys_project, sys_session)