<template>
  <div class="optional-section">
    <div class="toggle-bar">
      <div class="toggle-info">
        <span class="toggle-title">{{ title }}</span>
        <span class="toggle-hint">请确认系统是否涉及此部分内容</span>
      </div>
      <el-switch
        v-model="localEnabled"
        size="large"
        active-text="涉及"
        inactive-text="不涉及"
        inline-prompt
      />
    </div>
    <div v-if="enabled" class="section-body">
      <slot />
    </div>
    <div v-else class="section-empty">
      <div class="empty-icon">&#128207;</div>
      <p>本系统不涉及此部分，无需填写</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  enabled: Boolean,
  title: String,
})
const emit = defineEmits(['update:enabled', 'update:data'])

const localEnabled = computed({
  get: () => props.enabled,
  set: (val) => emit('update:enabled', val),
})
</script>

<style scoped>
.toggle-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 20px;
}

.toggle-title {
  font-size: 15px;
  font-weight: 600;
}

.toggle-hint {
  display: block;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.section-body {
  padding: 0;
}

.section-empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-icon { font-size: 40px; margin-bottom: 8px; }
</style>
