<template>
  <div class="section">
    <el-collapse v-model="activePanels">
      <el-collapse-item v-for="cfg in tableConfigs" :key="cfg.name" :title="cfg.title" :name="cfg.name">
        <TablePanel :config="cfg" v-model="localData[cfg.name]" />
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TablePanel from '../components/TablePanel.vue'
import { useSectionData } from '../composables/useSectionData.js'

const props = defineProps({ modelValue: { type: Object, default: () => ({}) } })
const activePanels = ref([])

const opt_importance = [
  { value: '关键', label: '关键' },
  { value: '重要', label: '重要' },
  { value: '一般', label: '一般' },
]

const opt_yes_no = [
  { value: '是', label: '是' },
  { value: '否', label: '否' },
]

const tableConfigs = [
  {
    name: 'table_4-1',
    title: '表4-1 工业控制系统基本情况',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '业务应用软件名称', label: '业务应用软件名称', span: 24 },
      { key: '系统架构', label: '系统架构', type: 'textarea', rows: 3, span: 24 },
      { key: '逻辑层次结构', label: '逻辑层次结构', type: 'textarea', rows: 3, span: 24 },
      { key: '流程工艺', label: '流程工艺', type: 'textarea', rows: 3, span: 24 },
      { key: '功能安全需求', label: '功能安全需求', type: 'textarea', rows: 3, span: 24 },
      { key: '安全组织架构', label: '安全组织架构', type: 'textarea', rows: 3, span: 24 },
      { key: '历史安全事件', label: '历史安全事件', type: 'textarea', rows: 3, span: 24 },
    ],
  },
  {
    name: 'table_4-2',
    title: '表4-2 工业控制系统设备资产',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络(逻辑)区域', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '品牌', label: '品牌', minWidth: 160 },
      { prop: '系统及版本', label: '系统及版本', minWidth: 160 },
      { prop: '设备类型', label: '设备类型/用途', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: '通信协议', label: '通信协议', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '1、重要程度填写关键、重要、一般；\n2、包括操作员站等监控设备，以及DCS、PLC、RTU等现场控制设备；\n3、如果采用虚拟化技术，且使用自建虚拟化管理平台，还需要填写宿主机的相关信息。',
  },
  {
    name: 'table_4-3',
    title: '表4-3 安全管理文档基本情况',
    type: 'checklist',
    showHeader: true,
    requirements: [
      '控制设备版本、补丁及固件更新前的测试报告或测评评估记录',
      '控制工业控制系统重要设备（含控制设备）及网络安全专用产品经相关部门安全性检测的检测报告',
    ],
  },
]

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>
