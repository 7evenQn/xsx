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

const opt_app_mode = [
  { value: 'B/S', label: 'B/S' },
  { value: 'C/S', label: 'C/S' },
]

const opt_dev_type = [
  { value: '自行开发', label: '自行开发' },
  { value: '外包开发', label: '外包开发' },
]

const opt_access_mode = [
  { value: '微信公众号', label: '微信公众号' },
  { value: '微信小程序', label: '微信小程序' },
  { value: 'APP', label: 'APP' },
]

const tableConfigs = [
  {
    name: 'table_6-1',
    title: '表6-1 无线接入设备基本情况调查',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 150 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络区域', minWidth: 160 },
      { prop: '系统及版本', label: '系统及版本', minWidth: 160 },
      { prop: '品牌型号', label: '品牌型号', minWidth: 160 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 150 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 150 },
      { prop: '是否热备', label: '是否热备', type: 'select', options: opt_yes_no, width: 150 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括无线接入网关等。',
  },
  {
    name: 'table_6-2',
    title: '表6-2 移动应用软件基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '业务名称', label: '业务(服务)名称', minWidth: 160 },
      { prop: '所属定级系统', label: '所属定级系统', minWidth: 160 },
      { prop: '应用软件及版本', label: '应用软件及版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '访问方式', label: '访问方式', type: 'select', options: opt_access_mode, width: 150 },
      { prop: '移动通信协议', label: '移动通信协议', minWidth: 160 },
      { prop: '开发方式', label: '自行开发/外包开发', type: 'select', options: opt_dev_type, width: 150 },
      { prop: '开发商', label: '开发商', minWidth: 160 },
      { prop: '用户类别及数量', label: '用户类别及数量', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 150 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },
  {
    name: 'table_6-3',
    title: '表6-3 移动终端基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '操作系统及版本', label: '操作系统及版本', minWidth: 160 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 150 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 150 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括专用移动终端。',
  },
]

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>
