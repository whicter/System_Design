---
hide:
  - navigation
  - toc
---

# System Design

<div class="sd-hero" markdown="0">
  <div class="sd-hero__inner">
    <div class="sd-hero__text">
      <div class="sd-hero__eyebrow">SYSTEM DESIGN · STAFF LEVEL</div>
      <h1 class="sd-hero__title">把系统讲清楚：<br>需求、取舍、失败与演进</h1>
      <p class="sd-hero__desc">Staff 级系统设计面试准备：评分点、45 / 60 分钟答题框架、核心积木与题库详解；外加九章、ByteByteGo 与 LeetCode 设计题等经典内容。</p>
      <div class="sd-hero__actions">
        <a class="sd-btn sd-btn--solid" href="_sections/s1/">从面试准备开始</a>
        <a class="sd-btn sd-btn--ghost" href="https://github.com/whicter/System_Design">GitHub</a>
      </div>
    </div>
    <svg class="sd-hero__diagram" viewBox="0 0 360 250" role="img" aria-label="Client, load balancer, services, cache, database and queue">
      <defs><marker id="sdarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#5eead4"/></marker></defs>
      <g fill="none" stroke="#5eead4" stroke-width="1.4" marker-end="url(#sdarrow)">
        <path d="M70 125 H112"/><path d="M178 125 H212"/><path d="M178 112 L212 70"/><path d="M178 138 L212 182"/>
        <path d="M280 70 V100"/><path d="M280 150 V170"/>
      </g>
      <g font-family="Inter, sans-serif" font-size="11" text-anchor="middle">
        <rect x="10" y="105" width="60" height="40" rx="8" fill="#0f2e2e" stroke="#2dd4bf"/><text x="40" y="129" fill="#ccfbf1">Client</text>
        <rect x="114" y="105" width="64" height="40" rx="8" fill="#0f2e2e" stroke="#2dd4bf"/><text x="146" y="123" fill="#ccfbf1">Load</text><text x="146" y="137" fill="#ccfbf1">Balancer</text>
        <rect x="214" y="45" width="132" height="34" rx="8" fill="#0f2e2e" stroke="#2dd4bf"/><text x="280" y="66" fill="#ccfbf1">Cache</text>
        <rect x="214" y="104" width="132" height="44" rx="8" fill="#134e4a" stroke="#5eead4"/><text x="280" y="122" fill="#f0fdfa">Services</text><text x="280" y="138" fill="#99f6e4" font-size="9">stateless · autoscaled</text>
        <rect x="214" y="172" width="62" height="34" rx="8" fill="#0f2e2e" stroke="#2dd4bf"/><text x="245" y="193" fill="#ccfbf1">DB</text>
        <rect x="284" y="172" width="62" height="34" rx="8" fill="#0f2e2e" stroke="#2dd4bf"/><text x="315" y="193" fill="#ccfbf1">Queue</text>
      </g>
    </svg>
  </div>
</div>

<div class="sd-strip" markdown="0">
  <div><b>45 / 60′</b><span>答题框架</span></div>
  <div><b>14+</b><span>核心积木</span></div>
  <div><b>题库</b><span>完整拆解与追问</span></div>
  <div><b>28</b><span>篇经典设计题</span></div>
</div>

<div class="sd-section-head">两大模块</div>

<!-- KB_MODULE_CARDS:rows -->
