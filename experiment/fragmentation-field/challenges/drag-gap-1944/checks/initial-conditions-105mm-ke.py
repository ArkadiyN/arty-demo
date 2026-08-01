m_oz = 0.035
v_fps = 2700
m_slug = m_oz / (16*32.174)
KE_ftlb = 0.5*m_slug*v_fps**2
print("KE (ft-lb) at r=20:", KE_ftlb)

# check a couple more ranges
for m_oz, v_fps, r in [(0.047,2430,30),(0.061,2220,40),(0.095,1920,60),(0.137,1750,80),(0.192,1550,100),(0.255,1420,120),(0.326,1320,140),(0.448,1200,170),(0.580,1120,200),(1.05,955,300)]:
    m_slug = m_oz/(16*32.174)
    KE = 0.5*m_slug*v_fps**2
    print(r, KE)
