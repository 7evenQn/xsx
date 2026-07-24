<template>
  <div id="app">
    <header class="app-header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">&#9733;</span>
          <span class="logo-text">资产填报系统</span>
        </div>
        <span class="header-subtitle">网络安全等级测评调研表</span>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --primary: #1a73e8;
  --primary-dark: #1557b0;
  --primary-light: #e8f0fe;
  --success: #0d9488;
  --warning: #d97706;
  --danger: #dc2626;
  --bg: #f0f2f5;
  --card-bg: #ffffff;
  --text: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --border: #e5e7eb;
  --radius: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.05);
  --shadow: 0 1px 3px rgba(0,0,0,.1), 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.06);
  --shadow-lg: 0 10px 15px rgba(0,0,0,.1), 0 4px 6px rgba(0,0,0,.05);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}

#app { min-height: 100vh; }

.app-header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2c5f8a 50%, #1e5a8a 100%);
  color: #fff;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}

.header-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 24px;
  height: 56px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: .5px;
}

.logo-icon {
  font-size: 24px;
  color: #60a5fa;
}

.header-subtitle {
  font-size: 13px;
  color: rgba(255,255,255,.65);
  padding-left: 16px;
  border-left: 1px solid rgba(255,255,255,.2);
}

.app-main {
  max-width: 1440px;
  margin: 0 auto;
  padding: 24px;
}

/* ── Global collapse panel styles ── */
.el-collapse {
  border: none !important;
}

.el-collapse-item {
  margin-bottom: 12px !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  background: #fff !important;
  transition: box-shadow .15s !important;
}

.el-collapse-item:hover {
  box-shadow: var(--shadow-sm) !important;
}

.el-collapse-item__header {
  height: 44px !important;
  padding: 0 16px !important;
  background: #fafbfc !important;
  border-bottom: 1px solid transparent !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  color: var(--text) !important;
}

.el-collapse-item__header:hover {
  background: #f1f5f9 !important;
}

.el-collapse-item.is-active .el-collapse-item__header {
  border-bottom-color: var(--border) !important;
  background: #fff !important;
}

.el-collapse-item__wrap {
  border: none !important;
  background: #fff !important;
}

.el-collapse-item__content {
  padding: 12px !important;
}

.el-collapse-item__header {
  position: relative !important;
}

.el-collapse-item__arrow {
  position: absolute !important;
  right: 16px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  margin: 0 !important;
}

/* ── Global table styles ── */
.el-table th.el-table__cell {
  background: #f1f5f9 !important;
  color: #334155 !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  border-bottom: 2px solid #cbd5e1 !important;
}

.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
  background: #fafbfc !important;
}

/* ── Global input focus rings ── */
.el-input__wrapper {
  box-shadow: 0 0 0 1px #e2e8f0 inset !important;
  border-radius: 4px !important;
  transition: box-shadow .15s !important;
}

.el-input__wrapper:hover {
  box-shadow: 0 0 0 1px #94a3b8 inset !important;
}

.el-input.is-focus .el-input__wrapper,
.el-input.is-focus .el-textarea__inner {
  box-shadow: 0 0 0 2px var(--primary) inset !important;
}

.el-textarea__inner {
  box-shadow: 0 0 0 1px #e2e8f0 inset !important;
  border-radius: 6px !important;
  transition: box-shadow .15s !important;
}

.el-textarea__inner:hover {
  box-shadow: 0 0 0 1px #94a3b8 inset !important;
}

.el-textarea__inner:focus {
  box-shadow: 0 0 0 2px var(--primary) inset !important;
}

/* ── Global tab styles ── */
.el-tabs__header {
  margin-bottom: 0 !important;
}

.el-tabs__nav-wrap::after {
  height: 1px !important;
  background: var(--border) !important;
}

.el-tabs__item.is-active {
  color: var(--primary) !important;
  font-weight: 600 !important;
}

.el-tabs__active-bar {
  background: var(--primary) !important;
  height: 3px !important;
  border-radius: 2px 2px 0 0 !important;
}
</style>
