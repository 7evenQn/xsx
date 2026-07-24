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

const tableConfigs = [
  {
    name: 'table_3-1',
    title: '表3-1 大数据形态',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '大数据形态', label: '大数据形态', type: 'checkbox', options: [
        { value: '大数据平台', label: '大数据平台' },
        { value: '大数据应用系统', label: '大数据应用系统' },
        { value: '大数据资源系统', label: '大数据资源系统' },
      ], span: 24 },
      { key: '运维所在地', label: '运维所在地', span: 12 },
      { key: '部署模式', label: '部署模式', type: 'radio', options: [
        { value: '公共大数据服务', label: '公共大数据服务' },
        { value: '私有大数据服务', label: '私有大数据服务' },
      ], span: 12 },
      { key: '大数据平台服务内容', label: '大数据平台服务内容', type: 'textarea', rows: 3, span: 24 },
    ],
  },
  {
    name: 'table_3-2',
    title: '表3-2 大数据平台测评情况',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '大数据平台名称', label: '大数据平台名称', span: 24 },
      { key: '等级测评结论', label: '等级测评结论', span: 12 },
      { key: '综合得分', label: '综合得分', span: 12 },
      { key: '报告编号', label: '报告编号', span: 24 },
      { key: '测评报告内容', label: '测评报告内容', type: 'textarea', rows: 4, span: 24 },
      { key: '整改情况描述', label: '整改情况描述', type: 'textarea', rows: 4, span: 24 },
    ],
    note: '大数据应用系统、大数据资源系统填写此表内容。',
  },
  {
    name: 'table_3-3',
    title: '表3-3 台服组件基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '台服组件名称', label: '台服组件名称', minWidth: 160 },
      { prop: '所在设备名称', label: '所在设备名称', minWidth: 160 },
      { prop: '品牌', label: '品牌', minWidth: 160 },
      { prop: '版本', label: '版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },
  {
    name: 'table_3-4',
    title: '表3-4 辅助工具基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '辅助工具名称', label: '辅助工具名称', minWidth: 160 },
      { prop: '所在设备名称', label: '所在设备名称', minWidth: 160 },
      { prop: '品牌', label: '品牌', minWidth: 160 },
      { prop: '版本', label: '版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },
  {
    name: 'table_3-5',
    title: '表3-5 资源管理平台基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '资源管理平台名称', label: '资源管理平台名称', minWidth: 160 },
      { prop: '所在设备名称', label: '所在设备名称', minWidth: 160 },
      { prop: '品牌', label: '品牌', minWidth: 160 },
      { prop: '版本', label: '版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址或URL', label: 'IP地址或URL地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },
  {
    name: 'table_3-6',
    title: '表3-6 数据基本信息',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '数据类别', label: '数据类别', minWidth: 160 },
      { prop: '数据级别', label: '数据级别', minWidth: 160 },
      { prop: '安全防护需求', label: '安全防护需求', minWidth: 160 },
      { prop: '数据采集', label: '数据采集', minWidth: 160 },
      { prop: '数据存储', label: '数据存储', minWidth: 160 },
      { prop: '数据处理', label: '数据处理', minWidth: 160 },
      { prop: '数据应用', label: '数据应用', minWidth: 160 },
      { prop: '数据流动', label: '数据流动', minWidth: 160 },
      { prop: '数据销毁', label: '数据销毁', minWidth: 160 },
    ],
  },
  {
    name: 'table_3-7',
    title: '表3-7 安全管理文档基本情况',
    type: 'checklist',
    showHeader: true,
    requirements: [
      '大数据平台相关资质及安全服务能力报告',
      '与大数据平台提供者签署的相关服务合同、协议或服务水平协议、安全声明等',
      '与数据交换、共享接收方签署的合同或协议',
    ],
  },
]

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>
