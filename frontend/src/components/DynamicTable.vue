<template>
  <div class="dynamic-table">
    <!-- Batch toolbar -->
    <div v-if="editable" class="batch-bar">
      <span class="batch-label">批量操作：</span>
      <el-input-number
        v-model="batchCount"
        :min="1"
        :max="50"
        :controls="false"
        size="small"
        style="width:100px"
      />
      <el-button type="primary" size="small" plain @click="batchAdd">批量添加行</el-button>
      <el-button
        v-if="selectedRows.length > 0"
        type="danger"
        size="small"
        plain
        @click="batchDelete"
      >
        批量删除 ({{ selectedRows.length }})
      </el-button>
      <el-button v-if="localRows.length > 0" type="info" size="small" plain @click="toggleAllSelection">
        {{ selectedRows.length === localRows.length ? '取消全选' : '全选' }}
      </el-button>
    </div>

    <div class="table-scroll-wrapper">
      <el-table
        ref="tableRef"
        :data="localRows"
        border
        stripe
        size="small"
        row-class-name="dt-row"
        @selection-change="onSelectionChange"
      >
      <el-table-column v-if="editable" type="selection" width="40" align="center" />
      <el-table-column type="index" label="序号" width="56" align="center" />
      <el-table-column
        v-for="col in columns"
        :key="col.prop"
        :prop="col.prop"
        :label="col.label"
        :width="col.width"
        :min-width="col.minWidth || 180"
      >
        <template #default="{ row, $index }">
          <template v-if="col.type === 'checkboxGroup'">
            <el-checkbox-group v-model="row[col.prop]" size="small" @change="onCellChange">
              <el-checkbox
                v-for="opt in col.options"
                :key="opt.value"
                :label="opt.value"
                :value="opt.value"
              >{{ opt.label }}</el-checkbox>
            </el-checkbox-group>
          </template>
          <template v-else-if="col.type === 'radio'">
            <el-radio-group v-model="row[col.prop]" size="small" @change="onCellChange">
              <el-radio
                v-for="opt in col.options"
                :key="opt.value"
                :value="opt.value"
              >{{ opt.label }}</el-radio>
            </el-radio-group>
          </template>
          <template v-else>
            <el-input
              v-model="row[col.prop]"
              size="small"
              :placeholder="col.placeholder || col.label"
              @input="onCellChange"
            />
          </template>
        </template>
      </el-table-column>
      <el-table-column v-if="editable" label="操作" width="72" fixed="right" align="center">
        <template #default="{ $index }">
          <el-button type="danger" size="small" text @click="removeRow($index)" class="del-btn">
            &#10005;
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    </div>

    <div v-if="localRows.length === 0 && editable" class="empty-hint">
      暂无数据，请通过上方「批量添加行」按钮添加
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  modelValue: { type: Array, default: () => [] },
  editable: { type: Boolean, default: true },
  defaultRows: { type: Number, default: 3 },
})

const emit = defineEmits(['update:modelValue'])

const tableRef = ref(null)
const batchCount = ref(1)
const selectedRows = ref([])

let uidCounter = 0

function emptyRow() {
  const row = { _uid: ++uidCounter }
  props.columns.forEach(c => {
    if (c.type === 'checkboxGroup') row[c.prop] = []
    else row[c.prop] = ''
  })
  return row
}

function initRows(val) {
  if (val && val.length > 0) {
    return val.map(r => {
      const base = emptyRow()
      return { ...base, ...r }
    })
  }
  return Array.from({ length: props.defaultRows }, () => emptyRow())
}

const localRows = ref(initRows(props.modelValue))

const suppressWatch = ref(false)

watch(() => props.modelValue, (val) => {
  if (suppressWatch.value) {
    suppressWatch.value = false
    return
  }
  localRows.value = initRows(val)
})

function emitAll() {
  suppressWatch.value = true
  const clean = localRows.value.map(r => {
    const row = {}
    for (const k of Object.keys(r)) {
      if (k === '_uid') continue
      const v = r[k]
      row[k] = Array.isArray(v) ? [...v] : v
    }
    return row
  })
  emit('update:modelValue', clean)
}

function onCellChange() {
  emitAll()
}

function addRow() {
  localRows.value.push(emptyRow())
  emitAll()
}

function removeRow(index) {
  localRows.value.splice(index, 1)
  emitAll()
}

function batchAdd() {
  for (let i = 0; i < batchCount.value; i++) {
    localRows.value.push(emptyRow())
  }
  emitAll()
}

function batchDelete() {
  const selectedUids = new Set(selectedRows.value.map(r => r._uid))
  localRows.value = localRows.value.filter(r => !selectedUids.has(r._uid))
  selectedRows.value = []
  emitAll()
}

function onSelectionChange(rows) {
  selectedRows.value = rows
}

function toggleAllSelection() {
  if (!tableRef.value) return
  if (selectedRows.value.length === localRows.value.length) {
    tableRef.value.clearSelection()
  } else {
    localRows.value.forEach(row => {
      tableRef.value.toggleRowSelection(row, true)
    })
  }
}

</script>

<style scoped>
.batch-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  padding: 0 2px;
}

.batch-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  white-space: nowrap;
}

.empty-hint {
  text-align: center;
  padding: 40px 16px;
  color: var(--text-muted);
  font-size: 13px;
}

.table-scroll-wrapper {
  overflow-x: auto;
  border-radius: 6px;
}

.table-scroll-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-scroll-wrapper::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 4px;
}

.table-scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

.dynamic-table :deep(.el-table) {
  border-radius: 6px;
}

.dynamic-table :deep(.el-table th.el-table__cell) {
  background: #f1f5f9 !important;
  color: #334155;
  font-weight: 600;
  font-size: 13px;
  border-bottom: 2px solid #cbd5e1;
}

.dynamic-table :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: #fafbfc;
}

.dynamic-table :deep(.el-table td.el-table__cell) {
  padding: 8px 0;
}

.dynamic-table :deep(.el-table .cell) {
  padding: 0 8px;
  white-space: nowrap;
}

/* ── Input inside table cells ── */
.dynamic-table :deep(.el-input__wrapper) {
  box-shadow: none;
  background: transparent;
  border-radius: 0;
  padding: 0 4px;
}

.dynamic-table :deep(.el-input__wrapper:hover) {
  box-shadow: none;
  background: #fafcff;
}

.dynamic-table :deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 2px 0 0 var(--primary) inset;
  background: #fff;
}

.del-btn {
  font-size: 16px;
  opacity: .4;
  transition: opacity .15s;
}

.del-btn:hover { opacity: 1; }
</style>


