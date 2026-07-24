<template>
  <div class="table-panel-shell">
    <FormHeader v-if="config.showHeader" />

    <!-- Single-row form type -->
    <div v-if="config.type === 'form'" class="form-panel">
      <!-- Dynamic form blocks (for expandable sections like table_1-10) -->
      <div v-for="(block, blockIdx) in formBlocks" :key="'block-'+blockIdx" class="form-block">
        <div v-if="config.dynamicLabel && formBlocks.length > 1" class="block-divider">
          <span>{{ config.dynamicLabel.replace('{n}', blockIdx + 1) }}</span>
          <el-button
            v-if="config.maxBlocks == null || formBlocks.length > 1"
            type="danger"
            size="small"
            text
            @click="removeBlock(blockIdx)"
          >&#10005;</el-button>
        </div>
        <el-form label-width="160px" label-position="left" class="styled-form">
          <el-row :gutter="20">
            <el-col
              v-for="field in config.fields"
              :key="field.key"
              :span="field.span || 12"
            >
              <el-form-item
                v-if="!field.condition || field.condition(localValue, block)"
                :label="field.label"
                class="form-item-custom"
              >
                <template v-if="field.type === 'checkbox'">
                  <el-checkbox-group v-model="block[field.key]" class="checkbox-group-pills">
                    <el-checkbox-button
                      v-for="opt in field.options"
                      :key="opt.value"
                      :value="opt.value"
                    >{{ opt.label }}</el-checkbox-button>
                  </el-checkbox-group>
                </template>
                <template v-else-if="field.type === 'radio'">
                  <el-radio-group v-model="block[field.key]" class="radio-group-pills">
                    <el-radio-button
                      v-for="opt in field.options"
                      :key="opt.value"
                      :value="opt.value"
                    >{{ opt.label }}</el-radio-button>
                  </el-radio-group>
                </template>
                <template v-else-if="field.type === 'textarea'">
                  <el-input v-model="block[field.key]" type="textarea" :rows="field.rows || 3" class="styled-textarea" />
                </template>
                <template v-else-if="field.type === 'date'">
                  <el-date-picker v-model="block[field.key]" type="date" class="styled-input" />
                </template>
                <template v-else-if="field.type === 'file'">
                  <input
                    type="file"
                    :ref="(el) => setUploadRef(field.key, el)"
                    :accept="field.accept || '.png,.jpg,.jpeg,.pdf'"
                    style="display:none"
                    @change="(e) => handleFileChange(e, block, field.key)"
                  />
                  <el-button type="primary" size="small" @click="triggerUpload(field.key)">
                    文件上传
                  </el-button>
                  <div v-if="block[field.key] && block[field.key].length > 0" class="upload-preview-list">
                    <div v-for="(f, fi) in block[field.key]" :key="fi" class="upload-preview-item">
                      <img
                        v-if="isImageFile(f.filename || f.url)"
                        :src="filePreviewUrl(f)"
                        class="upload-thumbnail"
                        @click="previewImage(f)"
                      />
                      <span v-else class="upload-file-icon">&#128206;</span>
                      <span class="upload-file-name">{{ f.filename || f.url?.split('/').pop() || '文件'+(fi+1) }}</span>
                      <el-button type="danger" size="small" text @click="removeFile(block, field.key, fi)">&#10005;</el-button>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <el-input v-model="block[field.key]" :placeholder="field.placeholder || '请输入'" class="styled-input" />
                </template>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      <!-- Add block button for dynamic forms -->
      <div v-if="config.dynamicLabel && (config.maxBlocks == null || formBlocks.length < config.maxBlocks)" style="margin-top:12px">
        <el-button type="primary" size="small" plain style="width:100%" @click="addBlock">
          + {{ config.addBlockLabel || '添加' }}
        </el-button>
      </div>
    </div>

    <!-- Dynamic table type -->
    <div v-else-if="config.type === 'table'" class="table-panel">
      <DynamicTable
        :columns="config.columns"
        :default-rows="config.defaultRows || 5"
        :editable="true"
        v-model="localValue"
      />
    </div>

    <!-- Checklist type -->
    <div v-else-if="config.type === 'checklist'" class="checklist-panel">
      <div class="batch-bar">
        <span class="batch-label">批量操作：</span>
        <el-input-number v-model="clBatchCount" :min="1" :max="50" :controls="false" size="small" style="width:100px" />
        <el-button type="primary" size="small" plain @click="clBatchAdd">批量添加行</el-button>
        <el-button v-if="clSelected.length > 0" type="danger" size="small" plain @click="clBatchDelete">
          批量删除 ({{ clSelected.length }})
        </el-button>
        <el-button v-if="checklistRows.length > 0" type="info" size="small" plain @click="clToggleAll">
          {{ clSelected.length === checklistRows.length ? '取消全选' : '全选' }}
        </el-button>
      </div>
      <el-table ref="clTableRef" :data="checklistRows" border size="small" stripe class="styled-table" @selection-change="onClSelectionChange">
        <el-table-column type="selection" width="40" align="center" />
        <el-table-column type="index" label="序号" width="56" align="center" />
        <el-table-column label="文档要求" min-width="200">
          <template #default="{ row }">
            <el-input v-model="row.requirement" size="small" placeholder="安全管理文档要求" disabled />
          </template>
        </el-table-column>
        <el-table-column label="文档名称" min-width="180">
          <template #default="{ row }">
            <el-input v-model="row[docNameKey]" size="small" placeholder="文档名称" />
          </template>
        </el-table-column>
        <el-table-column label="主要内容" min-width="180">
          <template #default="{ row }">
            <el-input v-model="row[contentKey]" size="small" placeholder="主要内容" />
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="120">
          <template #default="{ row }">
            <el-input v-model="row[remarkKey]" size="small" placeholder="备注" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="72" fixed="right" align="center">
          <template #default="{ $index }">
            <el-button type="danger" size="small" text @click="clRemoveRow($index)">&#10005;</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-button type="primary" size="small" plain style="margin-top:12px;width:100%" @click="addChecklistRow">
        + 添加条目
      </el-button>
    </div>

    <div v-if="config.note" class="note-box">
      <span class="note-icon">&#9432;</span>
      <span>{{ config.note }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import DynamicTable from './DynamicTable.vue'
import FormHeader from './FormHeader.vue'

const props = defineProps({
  config: { type: Object, required: true },
  modelValue: { type: [Object, Array], default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])

// ── Form-specific logic ──

const isDynamicForm = computed(() => props.config.type === 'form' && !!props.config.dynamicLabel)

const formBlocks = ref([{}])

watch(() => props.modelValue, (val) => {
  if (props.config.type !== 'form') return
  if (isDynamicForm.value) {
    if (val && Array.isArray(val.formBlocks) && val.formBlocks.length > 0) {
      formBlocks.value = val.formBlocks.map(b => ({ ...b }))
    } else {
      if (val && typeof val === 'object' && !Array.isArray(val) && Object.keys(val).length > 0) {
        formBlocks.value = [{ ...val }]
      } else {
        formBlocks.value = [buildEmptyBlock()]
      }
    }
  } else {
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      formBlocks.value = [{ ...val }]
    } else {
      formBlocks.value = [buildEmptyBlock()]
    }
  }
}, { immediate: true })

function buildEmptyBlock() {
  const block = {}
  if (props.config.fields) {
    props.config.fields.forEach(f => {
      if (f.type === 'checkbox') block[f.key] = []
      else if (f.type === 'file') block[f.key] = []
      else block[f.key] = ''
    })
  }
  return block
}

function syncFormToModel() {
  if (isDynamicForm.value) {
    emit('update:modelValue', { formBlocks: JSON.parse(JSON.stringify(formBlocks.value)) })
  } else {
    emit('update:modelValue', { ...formBlocks.value[0] })
  }
}

watch(formBlocks, () => {
  if (props.config.type !== 'form') return
  syncFormToModel()
}, { deep: true })

function addBlock() {
  formBlocks.value.push(buildEmptyBlock())
  syncFormToModel()
}

function removeBlock(idx) {
  if (formBlocks.value.length <= 1) return
  formBlocks.value.splice(idx, 1)
  syncFormToModel()
}

// ── Table / Checklist shared model bridge ──

const localValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

// ── File upload handlers ──

const uploadRefs = {}

function setUploadRef(key, el) {
  if (el) uploadRefs[key] = el
}

function triggerUpload(key) {
  uploadRefs[key]?.click()
}

async function handleFileChange(e, block, key) {
  const file = e.target.files?.[0]
  if (!file) return

  const allowed = ['.png', '.jpg', '.jpeg', '.pdf']
  const ext = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowed.includes(ext)) {
    ElMessage.error('仅支持 png/jpg/jpeg/pdf 格式')
    e.target.value = ''
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过10MB')
    e.target.value = ''
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('/api/upload', { method: 'POST', body: formData })
    if (!res.ok) throw new Error('Upload failed')
    const data = await res.json()

    if (!block[key]) block[key] = []
    if (Array.isArray(block[key])) {
      block[key].push({ url: data.url, filename: data.filename, size: data.size })
    } else {
      block[key] = [{ url: data.url, filename: data.filename, size: data.size }]
    }
    syncFormToModel()
    ElMessage.success('文件上传成功')
  } catch {
    ElMessage.error('文件上传失败')
  }

  e.target.value = ''
}

function isImageFile(filename) {
  if (!filename) return false
  return /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(filename)
}

function filePreviewUrl(f) {
  if (!f) return ''
  // If there's a local blob URL stored, use it directly
  if (f.blobUrl) return f.blobUrl
  // Otherwise, use the server URL - for images served by the backend
  const url = f.url || ''
  if (url.startsWith('/uploads/')) return url
  return url
}

function previewImage(f) {
  const url = filePreviewUrl(f)
  if (!url) return
  window.open(url, '_blank')
}

function removeFile(block, key, index) {
  if (!Array.isArray(block[key])) return
  block[key].splice(index, 1)
  syncFormToModel()
}

// ── Checklist-specific ──

const clTableRef = ref(null)
const clBatchCount = ref(1)
const clSelected = ref([])

const checklistRows = computed(() => {
  if (!Array.isArray(props.modelValue)) return []
  return props.modelValue
})

const docNameKey = computed(() => props.config.fieldKeys?.docName || '文档名称')
const contentKey = computed(() => props.config.fieldKeys?.content || '主要内容')
const remarkKey = computed(() => props.config.fieldKeys?.remark || '备注')

function makeChecklistRow() {
  const row = { requirement: '' }
  row[docNameKey.value] = ''
  row[contentKey.value] = ''
  row[remarkKey.value] = ''
  return row
}

// Auto-populate checklist from config requirements when data is empty
let clInitialized = false
watch(
  () => props.config.requirements,
  (requirements) => {
    if (props.config.type !== 'checklist') return
    if (!requirements || !Array.isArray(requirements) || requirements.length === 0) return
    if (clInitialized) return
    const current = props.modelValue
    if (!Array.isArray(current) || current.length === 0) {
      const rows = requirements.map(req => {
        const row = makeChecklistRow()
        row.requirement = req
        return row
      })
      clInitialized = true
      emit('update:modelValue', rows)
    } else {
      clInitialized = true
    }
  },
  { immediate: true }
)

function addChecklistRow() {
  const newVal = [...checklistRows.value, makeChecklistRow()]
  emit('update:modelValue', newVal)
}

function clBatchAdd() {
  const current = [...checklistRows.value]
  for (let i = 0; i < clBatchCount.value; i++) {
    current.push(makeChecklistRow())
  }
  emit('update:modelValue', current)
}

function clRemoveRow(idx) {
  const newVal = [...checklistRows.value]
  newVal.splice(idx, 1)
  emit('update:modelValue', newVal)
}

function onClSelectionChange(rows) {
  clSelected.value = rows
}

function clBatchDelete() {
  const selectedSet = new Set(clSelected.value)
  const newVal = checklistRows.value.filter(r => !selectedSet.has(r))
  clSelected.value = []
  emit('update:modelValue', newVal)
}

function clToggleAll() {
  if (!clTableRef.value) return
  if (clSelected.value.length === checklistRows.value.length) {
    clTableRef.value.clearSelection()
  } else {
    checklistRows.value.forEach(row => {
      clTableRef.value.toggleRowSelection(row, true)
    })
  }
}
</script>

<style scoped>
.table-panel-shell {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

/* ── Form panel ── */
.form-panel {
  padding: 20px 24px;
}

.form-block {
  margin-bottom: 8px;
}

.block-divider {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  margin-bottom: 4px;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
  border-bottom: 2px solid var(--primary-light);
}

.styled-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.styled-input :deep(.el-input__wrapper),
.styled-textarea :deep(.el-textarea__inner) {
  box-shadow: 0 0 0 1px #e2e8f0 inset;
  border-radius: 6px;
  transition: box-shadow .15s;
}

.styled-input :deep(.el-input__wrapper:hover),
.styled-textarea :deep(.el-textarea__inner:hover) {
  box-shadow: 0 0 0 1px #94a3b8 inset;
}

.styled-input :deep(.el-input.is-focus .el-input__wrapper),
.styled-textarea :deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 2px var(--primary) inset;
}

/* Checkbox / Radio pill groups */
.checkbox-group-pills :deep(.el-checkbox-button__inner),
.radio-group-pills :deep(.el-radio-button__inner) {
  border-radius: 4px !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: none !important;
  font-size: 12px;
  padding: 4px 14px;
  transition: all .15s;
}

.checkbox-group-pills :deep(.el-checkbox-button.is-checked .el-checkbox-button__inner),
.radio-group-pills :deep(.el-radio-button.is-active .el-radio-button__inner) {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
}


/* ── Upload preview ── */
.upload-preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.upload-preview-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 12px;
}

.upload-thumbnail {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #e2e8f0;
}

.upload-thumbnail:hover {
  border-color: var(--primary);
}

.upload-file-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.upload-file-name {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-secondary);
}

/* ── Table panel ── */
.table-panel {
  padding: 16px;
}

/* ── Batch bar ── */
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

/* ── Checklist panel ── */
.checklist-panel {
  padding: 16px;
}

.styled-table :deep(.el-table th.el-table__cell) {
  background: #f1f5f9 !important;
  color: #334155;
  font-weight: 600;
  font-size: 13px;
  border-bottom: 2px solid #cbd5e1;
}

.styled-table :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: #fafbfc;
}

/* ── Note box ── */
.note-box {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 0 16px 16px;
  padding: 12px 16px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 6px;
  font-size: 13px;
  color: #92400e;
  line-height: 1.6;
  white-space: pre-line;
}

.note-icon {
  flex-shrink: 0;
  font-size: 16px;
  color: #f59e0b;
  margin-top: 1px;
}
</style>
