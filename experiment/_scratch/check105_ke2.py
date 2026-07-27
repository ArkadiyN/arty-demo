def ke_ftlb(m_oz, v_fps):
    m_slug = m_oz/16/32.174
    return 0.5*m_slug*v_fps**2

# sequence A (odd raw lines) -- originally labeled "Table 52 perforation"
seqA = [
    (20,.010,2440),(30,.014,2060),(40,.019,1770),(60,.030,1410),(80,.043,1180),
    (100,.192,1550),(150,.083,846),(200,.109,738),(300,.166,598),(400,.232,507),(500,.312,438)
]
print("Sequence A (odd raw lines):")
for r,m,v in seqA:
    print(f"  r={r:4} m={m:.3f} v={v:5} KE={ke_ftlb(m,v):.1f} ft-lb")

seqB = [
    (20,.035,2700),(30,.047,2430),(40,.061,2220),(60,.095,1920),(80,.137,1750),
    (100,.055,1040),(120,.255,1420),(140,.326,1320),(170,.448,1200),(200,.580,1120),(300,1.05,955)
]
print("\nSequence B (even raw lines), r=100 UNCORRECTED (native .055/1040):")
for r,m,v in seqB:
    print(f"  r={r:4} m={m:.3f} v={v:5} KE={ke_ftlb(m,v):.1f} ft-lb")
