import { ref, watch, toRef } from 'vue'

/**
 * Shared logic for section views: build default data, watch prop changes, expose getData.
 * @param {Array} tableConfigs - static table config array
 * @param {Object} props - component props (must contain modelValue)
 * @returns {{ localData, getData }}
 */
export function useSectionData(tableConfigs, props) {
  function buildDefaultData(source) {
    const data = {}
    tableConfigs.forEach(cfg => {
      const existing = source?.[cfg.name]
      const isChecklist = cfg.type === 'checklist' && cfg.requirements && cfg.requirements.length > 0
      const isEmptyExisting = !existing || (Array.isArray(existing) && existing.length === 0)
      if (isChecklist && isEmptyExisting) {
        const fieldKeys = cfg.fieldKeys || {}
        const docNameKey = fieldKeys.docName || '文档名称'
        const contentKey = fieldKeys.content || '主要内容'
        const remarkKey = fieldKeys.remark || '备注'
        data[cfg.name] = cfg.requirements.map(req => {
          const row = { requirement: req }
          row[docNameKey] = ''
          row[contentKey] = ''
          row[remarkKey] = ''
          return row
        })
      } else if (existing !== undefined && existing !== null) {
        data[cfg.name] = JSON.parse(JSON.stringify(existing))
      } else {
        data[cfg.name] = cfg.type === 'table' || cfg.type === 'checklist' ? [] : {}
      }
    })
    return data
  }

  const modelRef = toRef(props, 'modelValue')
  const localData = ref(buildDefaultData(modelRef.value))

  watch(modelRef, (newVal) => {
    localData.value = buildDefaultData(newVal)
  }, { deep: true })

  function getData() {
    return JSON.parse(JSON.stringify(localData.value))
  }

  return { localData, getData }
}
