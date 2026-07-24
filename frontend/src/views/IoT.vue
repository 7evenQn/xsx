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
    name: 'table_5-1',
    title: '表5-1 节点物理信息',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '节点名称', label: '节点名称', minWidth: 160 },
      { prop: '地址', label: '地址', minWidth: 160 },
      { prop: '部署设备类型及数量', label: '部署设备类型及数量', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 140 },
      { prop: '室内/室外', label: '室内/室外', minWidth: 160 },
    ],
  },
  {
    name: 'table_5-2',
    title: '表5-2 网关节点设备信息',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '激活认证状态', label: '激活/认证状态', minWidth: 160 },
      { prop: '设备序列编号', label: '设备序列编号', minWidth: 160 },
      { prop: '软硬件版本', label: '软件/硬件版本', minWidth: 160 },
      { prop: '物理地址', label: '物理地址（MAC）', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址/掩码/端口', minWidth: 160 },
      { prop: '网关', label: '网关', minWidth: 160 },
      { prop: '类型', label: '类型', minWidth: 160 },
      { prop: '所在物理位置', label: '所在物理位置', minWidth: 160 },
      { prop: '使用通信协议', label: '使用通信协议', minWidth: 160 },
      { prop: '设备检测情况', label: '设备检测情况（周期/方式）', minWidth: 160 },
    ],
  },
  {
    name: 'table_5-3',
    title: '表5-3 感知节点设备信息',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '激活认证状态', label: '激活/认证状态', minWidth: 160 },
      { prop: '设备序列编号', label: '设备序列编号', minWidth: 160 },
      { prop: '软硬件版本', label: '软件/硬件版本', minWidth: 160 },
      { prop: '物理地址', label: '物理地址（MAC）', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址/掩码/端口', minWidth: 160 },
      { prop: '网关', label: '网关', minWidth: 160 },
      { prop: '类型', label: '类型', minWidth: 160 },
      { prop: '所在物理位置', label: '所在物理位置', minWidth: 160 },
      { prop: '使用通信协议', label: '使用通信协议', minWidth: 160 },
      { prop: '设备检测情况', label: '设备检测情况（周期/方式）', minWidth: 160 },
    ],
    note: '包括传感器、RFID标签等。',
  },
  {
    name: 'table_5-4',
    title: '表5-4 安全管理文档基本情况',
    type: 'checklist',
    showHeader: true,
    requirements: [
      '感知节点设备所处物理环境的设计或验收文档',
      '感知节点设备（关键网关节点设备）电力供应设计或验收文档',
      '电力供应措施的运行维护记录',
      '感知层安全设计文档',
      '感知节点设备、网关节点设备部署环境维护记录',
      '感知节点、网关节点设备安全管理文档',
      '感知节点设备、网关节点设备部署环境管理文档',
      '感知节点设备、网关节点设备部署环境的相关保密性管理记录',
    ],
  },
]

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>
