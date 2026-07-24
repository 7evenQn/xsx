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

const tableConfigs = [
  {
    name: 'table_2-1',
    title: '表2-1 云计算形态',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '云计算形态', label: '云计算形态', type: 'checkbox', options: [
        { value: '云计算平台', label: '云计算平台' },
        { value: '云服务客户业务应用系统', label: '云服务客户业务应用系统' },
      ], span: 24 },
      { key: '云部署模式', label: '云部署模式', type: 'radio', options: [
        { value: '公有云', label: '公有云' }, { value: '私有云', label: '私有云' }, { value: '混合云', label: '混合云' },
      ], span: 24 },
      { key: '云服务模式', label: '云服务模式', type: 'checkbox', options: [
        { value: 'IaaS', label: 'IaaS' }, { value: 'PaaS', label: 'PaaS' }, { value: 'SaaS', label: 'SaaS' },
      ], span: 24 },
      { key: '运维所在地', label: '运维所在地', span: 12 },
      { key: '物理机房所在地', label: '物理机房所在地', span: 12 },
      { key: '业务应用系统使用资源情况', label: '业务应用系统使用资源情况', type: 'textarea', rows: 3, span: 24 },
      { key: '云计算平台运营机构与云租户关系', label: '云计算平台运营机构与云租户关系', span: 24 },
      { key: '云计算平台服务内容', label: '云计算平台服务内容', type: 'textarea', rows: 3, span: 24 },
    ],
  },
  {
    name: 'table_2-2',
    title: '表2-2 云计算平台测评情况',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '云计算平台名称', label: '云计算平台名称', span: 12 },
      { key: '云计算平台安全保护等级', label: '云计算平台安全保护等级', span: 12 },
      { key: '等级测评结论', label: '等级测评结论', span: 12 },
      { key: '综合得分', label: '综合得分', span: 12 },
      { key: '报告编号', label: '报告编号', span: 24 },
      { key: '测评报告内容', label: '云计算平台测评报告内容', type: 'textarea', rows: 4, span: 24 },
      { key: '整改情况描述', label: '云计算平台整改情况描述', type: 'textarea', rows: 4, span: 24 },
    ],
    note: '云租户系统填写此表内容。',
  },
  {
    name: 'table_2-3',
    title: '表2-3 安全管理文档基本情况',
    type: 'checklist',
    showHeader: true,
    requirements: [
      '与云服务商签署的相关服务合同、服务水平协议、保密协议',
      '供应链安全事件报告或威胁报告',
      '供应商重要变更方案和变更记录',
    ],
  },
]

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>
