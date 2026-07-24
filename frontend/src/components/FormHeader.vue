<template>
  <div class="form-header">
    <div class="form-header-inner">
      <div class="header-icon">&#9998;</div>
      <div class="header-fields">
        <div class="field-item">
          <label>填表人</label>
          <el-input v-model="filler" size="small" placeholder="姓名" />
        </div>
        <div class="field-divider"></div>
        <div class="field-item">
          <label>日期</label>
          <el-date-picker v-model="date" type="date" size="small" placeholder="选择日期" />
        </div>
      </div>
    </div>
    <slot />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const filler = ref('')
const date = ref('')
</script>

<style scoped>
.form-header { width: 100%; margin-bottom: 8px; }

.form-header-inner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: #f0f4ff;
  border: 1px solid #dbeafe;
  border-radius: var(--radius);
}

.header-icon {
  font-size: 18px;
  color: var(--primary);
  opacity: .6;
}

.header-fields {
  display: flex;
  align-items: center;
  gap: 4px;
}

.field-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.field-item label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  white-space: nowrap;
}

.field-divider {
  width: 1px;
  height: 20px;
  background: #cbd5e1;
  margin: 0 12px;
}
</style>
