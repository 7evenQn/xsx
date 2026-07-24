<template>
  <div class="section">
    <el-collapse v-model="activePanels" class="styled-collapse">
      <el-collapse-item
        v-for="cfg in tableConfigs"
        :key="cfg.name"
        :name="cfg.name"
      >
        <template #title>
          <div class="collapse-title">
            <span class="collapse-num">{{ cfg.name.replace('table_', '') }}</span>
            <span>{{ cfg.title }}</span>
          </div>
        </template>
        <TablePanel
          :config="cfg"
          v-model="localData[cfg.name]"
        />
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

const { localData, getData } = useSectionData(tableConfigs, props)
defineExpose({ getData })
</script>

<!-- ── Static config (outside component to avoid recreation) ── -->

<script>
const opt_importance = [
  { value: '关键', label: '关键' },
  { value: '重要', label: '重要' },
  { value: '一般', label: '一般' },
]

const opt_yes_no = [
  { value: '是', label: '是' },
  { value: '否', label: '否' },
]

const opt_unit_type = [
  { value: '党政机关', label: '党政机关' },
  { value: '国家重要行业、重要领域或重要企事业单位', label: '国家重要行业、重要领域或重要企事业单位' },
  { value: '一般企事业单位', label: '一般企事业单位' },
  { value: '其它类型', label: '其它类型' },
]

const opt_sys_form = [
  { value: '传统IT系统', label: '传统IT系统' },
  { value: '云计算', label: '云计算' },
  { value: '采用移动互联技术的系统', label: '采用移动互联技术的系统' },
  { value: '物联网', label: '物联网' },
  { value: '工业控制系统', label: '工业控制系统' },
  { value: '大数据', label: '大数据' },
]

const opt_app_mode = [
  { value: 'B/S', label: 'B/S' },
  { value: 'C/S', label: 'C/S' },
]

const opt_dev_type = [
  { value: '自行开发', label: '自行开发' },
  { value: '外包开发', label: '外包开发' },
]

const tableConfigs = [
  // ── 表1-1: 单位基本情况 ──
  {
    name: 'table_1-1',
    title: '表1-1 单位基本情况',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '公司名称', label: '单位全称', span: 8 },
      { key: '公司简称', label: '简称', span: 4 },
      { key: '单位情况简介', label: '单位情况简介', type: 'textarea', rows: 3, span: 24 },
      { key: '单位所属类型', label: '单位所属类型', type: 'checkbox', options: opt_unit_type, span: 24 },
      { key: '其它类型说明', label: '其他类型说明（勾选"其它类型"后填写）', type: 'textarea', rows: 2, span: 24, condition: (_, data) => (data['单位所属类型'] || []).includes('其它类型') },
      { key: '单位地址', label: '单位地址', span: 18 },
      { key: '邮编', label: '邮政编码', span: 6 },
      { key: '负责人姓名', label: '负责人姓名', span: 6 },
      { key: '电话1', label: '负责人电话', span: 6 },
      { key: '传真1', label: '负责人传真', span: 4 },
      { key: '所属部门1', label: '负责人所属部门', span: 4 },
      { key: '邮件1', label: '负责人电子邮件', span: 4 },
      { key: '联系人姓名', label: '联系人姓名', span: 6 },
      { key: '电话2', label: '联系人电话', span: 6 },
      { key: '传真2', label: '联系人传真', span: 4 },
      { key: '所属部门2', label: '联系人所属部门', span: 4 },
      { key: '邮件2', label: '联系人电子邮件', span: 4 },
      { key: '上级主管部门', label: '上级主管部门', span: 24 },
    ],
    note: '请填写与被测评系统有关的机构的内容。',
  },

  // ── 表1-2: 等级保护对象基本情况 ──
  {
    name: 'table_1-2',
    title: '表1-2 等级保护对象基本情况',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '等级保护对象名称', label: '等级保护对象名称', span: 12 },
      { key: '安全保护等级', label: '安全保护等级', span: 6 },
      { key: '业务信息安全保护等级', label: '业务信息安全保护等级', span: 6 },
      { key: '系统服务安全保护等级', label: '系统服务安全保护等级', span: 6 },
      { key: '等级保护对象形态', label: '等级保护对象形态', type: 'checkbox', options: opt_sys_form, span: 24 },
      { key: '备案证明编号', label: '备案证明编号', span: 12 },
      { key: '备案证明扫描件', label: '备案证明扫描件', type: 'file', span: 24 },
      { key: '功能描述', label: '功能描述', type: 'textarea', rows: 4, span: 24 },
    ],
    note: '1、定级对象名称、安全保护等级、业务信息安全保护等级、系统服务安全保护等级、功能描述需与定级报告保持一致；\n2、备案证明编号为受理公安机构反馈的备案证明上的编号；\n3、如果等级保护对象采用虚拟化技术，且使用的虚拟化管理平台为第三方单位提供，在"等级保护对象形态"中需勾选"云计算"。',
  },

  // ── 表1-3: 机房 ──
  {
    name: 'table_1-3',
    title: '表1-3 机房',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '机房名称', label: '机房名称', minWidth: 160 },
      { prop: '物理位置', label: '物理位置', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', minWidth: 140 },
    ],
  },

  // ── 表1-4: 网络拓扑图及网络描述 ──
  {
    name: 'table_1-4',
    title: '表1-4 网络拓扑图及网络描述',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '网络拓扑结构图', label: '网络拓扑结构图', type: 'file', span: 24 },
      { key: '网络拓扑文字描述', label: '网络拓扑文字描述', type: 'textarea', rows: 6, span: 24 },
    ],
  },

  // ── 表1-5: 网络结构情况 ──
  {
    name: 'table_1-5',
    title: '表1-5 网络结构情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '网络区域名称', label: '网络区域名称', minWidth: 160 },
      { prop: '区域功能描述', label: '区域功能描述', minWidth: 160 },
      { prop: 'IP网段地址', label: 'IP网段地址', minWidth: 160 },
      { prop: '服务器数量', label: '服务器数量', width: 130 },
      { prop: '终端数量', label: '终端数量（管理）', width: 130 },
      { prop: '与其连接的其它网络区域', label: '与其连接的其它网络区域', minWidth: 160 },
      { prop: '网络区域边界设备', label: '网络区域边界设备', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '责任部门', label: '责任部门', minWidth: 160 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },

  // ── 表1-6: 网络外连情况 ──
  {
    name: 'table_1-6',
    title: '表1-6 网络外连情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '外联线路名称', label: '外联线路名称（边界名称）', minWidth: 160 },
      { prop: '所属网络区域', label: '所属网络区域', minWidth: 160 },
      { prop: '连接对象名称', label: '连接对象名称', minWidth: 160 },
      { prop: '接入线路种类', label: '接入线路种类', minWidth: 160 },
      { prop: '传输速率', label: '传输速率（带宽）', minWidth: 160 },
      { prop: '线路接入设备', label: '线路接入设备', minWidth: 160 },
      { prop: '承载主要业务应用', label: '承载主要业务应用', minWidth: 160 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },

  // ── 表1-7: 网络互联设备基本情况 ──
  {
    name: 'table_1-7',
    title: '表1-7 网络互联设备基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络区域', minWidth: 160 },
      { prop: '系统及版本', label: '系统及版本', minWidth: 160 },
      { prop: '品牌型号', label: '品牌型号', minWidth: 160 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '是否热备', label: '是否热备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括交换机、路由器、负载均衡、IPV4/IPV6转换设备等。',
  },

  // ── 表1-8: 安全设备基本情况调查 ──
  {
    name: 'table_1-8',
    title: '表1-8 安全设备基本情况调查',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络区域', minWidth: 160 },
      { prop: '系统及版本', label: '系统及版本', minWidth: 160 },
      { prop: '品牌型号', label: '品牌型号', minWidth: 160 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '是否热备', label: '是否热备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括防火墙、入侵检测设备、终端威胁感知平台、无线接入网关、移动终端安全管理系统等。',
  },

  // ── 表1-9: 业务应用基本情况 ──
  {
    name: 'table_1-9',
    title: '表1-9 业务应用基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '业务名称', label: '业务(服务)名称', minWidth: 160 },
      { prop: '所属定级系统', label: '所属定级系统', minWidth: 160 },
      { prop: '业务应用软件及版本', label: '业务应用软件及版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '应用模式', label: '应用模式(B/S或C/S)', type: 'select', options: opt_app_mode, width: 160 },
      { prop: '硬件软件平台', label: '硬件/软件平台', minWidth: 160 },
      { prop: '自行开发外包开发', label: '自行开发/外包开发', type: 'select', options: opt_dev_type, width: 160 },
      { prop: '开发商', label: '开发商', minWidth: 160 },
      { prop: '用户类别及数量', label: '用户类别及数量', minWidth: 160 },
      { prop: 'URL地址', label: 'URL地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
  },

  // ── 表1-10: 应用处理流程 ──
  {
    name: 'table_1-10',
    title: '表1-10 应用处理流程',
    type: 'form',
    showHeader: true,
    dynamicLabel: '业务应用软件 {n}',
    addBlockLabel: '添加业务应用软件',
    maxBlocks: 10,
    fields: [
      { key: '业务应用软件名称', label: '业务应用软件名称', span: 12 },
      { key: '应用处理流程图', label: '应用处理流程图', type: 'file', span: 12 },
    ],
    note: '业务应用软件应该描绘处理流程图，说明主要处理步骤、过程、流向、涉及设备和用户。如本页不够，请继续添加业务应用软件。',
  },

  // ── 表1-11: 主要业务数据流程 ──
  {
    name: 'table_1-11',
    title: '表1-11 主要业务数据流程',
    type: 'form',
    showHeader: true,
    dynamicLabel: '业务数据 {n}',
    addBlockLabel: '添加业务数据',
    maxBlocks: 10,
    fields: [
      { key: '数据名称', label: '数据名称', span: 12 },
      { key: '数据流程图', label: '数据流程图', type: 'file', span: 12 },
    ],
    note: '从不同类型业务用户视角出发，给出关键业务处理流程图，并标注涉及应用组件/模块、主要处理动作，以及关键业务数据在主机设备（程序模块）之间的交换情况。',
  },

  // ── 表1-12: 服务器基本情况 ──
  {
    name: 'table_1-12',
    title: '表1-12 服务器基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '所属业务系统', label: '所属业务系统/平台名称', minWidth: 160 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络(逻辑)区域', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '操作系统及版本', label: '操作系统及版本', minWidth: 160 },
      { prop: '数据库及版本', label: '数据库管理系统及版本', minWidth: 160 },
      { prop: '中间件及版本', label: '中间件及版本', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '是否热备', label: '是否热备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '1、包括服务器、存储设备等；\n2、如果采用虚拟化技术，且使用自建虚拟化管理平台，需要填写宿主机的相关信息。',
  },

  // ── 表1-13: 终端基本情况 ──
  {
    name: 'table_1-13',
    title: '表1-13 终端基本情况',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '设备名称', label: '设备名称', minWidth: 160 },
      { prop: '物理区域', label: '物理区域', minWidth: 160 },
      { prop: '网络区域', label: '网络(逻辑)区域', minWidth: 160 },
      { prop: '是否虚拟设备', label: '是否虚拟设备', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '操作系统及版本', label: '操作系统/控制软件及版本', minWidth: 160 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址', label: 'IP地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '1、重要程度填写关键、重要、一般；\n2、包括业务终端、运维终端、管理终端等；\n3、如果采用虚拟化技术，且使用自建虚拟化管理平台，还需要填写宿主机的相关信息。',
  },

  // ── 表1-14: 系统管理软件/平台 ──
  {
    name: 'table_1-14',
    title: '表1-14 系统管理软件/平台',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '软件名称', label: '系统管理软件/平台名称', minWidth: 160 },
      { prop: '所在设备名称', label: '所在设备名称', minWidth: 160 },
      { prop: '版本', label: '版本', minWidth: 160 },
      { prop: '主要功能', label: '主要功能', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: 'IP地址或URL', label: 'IP地址或URL地址', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括数据库、中间件、网管软件/平台、安管软件/平台、虚拟化管理软件、云计算管理软件/平台等。',
  },

  // ── 表1-15: 数据资源 ──
  {
    name: 'table_1-15',
    title: '表1-15 数据资源',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '数据类别', label: '数据类别', minWidth: 160 },
      { prop: '所属业务应用', label: '所属业务应用', minWidth: 160 },
      { prop: '安全防护需求', label: '安全防护需求', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备份方式', label: '备份方式', minWidth: 160 },
      { prop: '备份频率', label: '备份频率', width: 130 },
      { prop: '备份介质', label: '备份介质', width: 130 },
      { prop: '保存期', label: '保存期', width: 130 },
      { prop: '是否异地保存', label: '是否异地保存', type: 'select', options: opt_yes_no, width: 130 },
      { prop: '过期处理方法', label: '过期处理方法', minWidth: 160 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '1、数据类别包括鉴别数据、重要业务数据、重要审计数据、重要配置数据和重要个人信息等；\n2、安全防护需求一般从保密性、完整性等方面进行分析；\n3、重要程度填写关键、重要、一般。',
  },

  // ── 表1-16: 密码产品 ──
  {
    name: 'table_1-16',
    title: '表1-16 密码产品',
    type: 'table',
    showHeader: true,
    defaultRows: 3,
    columns: [
      { prop: '产品名称', label: '产品/模块名称', minWidth: 160 },
      { prop: '生产厂商', label: '生产厂商', minWidth: 160 },
      { prop: '商密型号', label: '商密型号', minWidth: 160 },
      { prop: '认证证书编号', label: '商密产品认证证书编号', minWidth: 160 },
      { prop: '使用的密码算法', label: '使用的密码算法', minWidth: 160 },
      { prop: '数量', label: '数量(台/套)', width: 130 },
      { prop: '用途', label: '用途', minWidth: 160 },
      { prop: '重要程度', label: '重要程度', type: 'select', options: opt_importance, width: 130 },
      { prop: '备注', label: '备注', minWidth: 160 },
    ],
    note: '包括VPN、数字证书、令牌、密码机等。',
  },

  // ── 表1-17: 安全相关人员 ──
  {
    name: 'table_1-17',
    title: '表1-17 安全相关人员',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '姓名', label: '姓名', minWidth: 120 },
      { prop: '部门岗位', label: '部门/岗位/角色', minWidth: 160 },
      { prop: '联系方式', label: '联系方式', minWidth: 160 },
      { prop: '所属单位', label: '所属单位', minWidth: 160 },
      { prop: '负责范围', label: '负责范围', minWidth: 160 },
    ],
    note: '包括安全主管、网络管理员、系统管理员、应用管理员、数据管理员、审计管理员、机房管理员、资产管理员等。',
  },

  // ── 表1-18: 安全管理文档（拆为6个子面板） ──
  {
    name: 'table_1-18a',
    title: '表1-18 安全管理文档 - 安全物理环境',
    type: 'checklist',
    showHeader: true,
    requirements: [
      '机房安全管理制度',
      '机房安全设计和验收方面的文档',
      '机房值守记录以及进出机房的人员登记记录',
      '来访人员进入机房的审批记录',
      '机房日常巡检记录',
      '电子门禁系统验收文档或产品安全认证资质',
      '电子门禁系统运行和维护记录',
      '监控进入机房的电子门禁系统记录',
      '机房防盗报警设施运行径路、报警记录和维护记录',
      '机房的摄像、传感等监控报警系统运行记录、监控记录、报警记录和维护记录',
      '机房防盗报警设施和监控报警设施的安全资质材料、安装测试和验收报告',
      '自动消防系统的运行记录、报警记录、定期检查和维修记录',
      '机房湿度记录、防水防潮处理记录和除湿装置运行记录',
      '水敏感检测仪表或元件的运行记录',
      '温湿度自动调节设施的温湿度记录、运行记录和维护记录',
      '稳压器、过电压防护设备、短期备用电源设备检查和维护记录',
      '备用供电系统的检查和维护记录、运行记录',
      '冗余或并行的电力电缆线路切换记录',
      '计算机系统供电的运行记录',
    ],
  },
  {
    name: 'table_1-18b',
    title: '表1-18 安全管理文档 - 安全管理制度',
    type: 'checklist',
    requirements: [
      '机构总体安全方针和政策方面的管理制度',
      '日常管理操作的操作规程',
      '管理制度、操作规程修订、维护方面的管理制度',
      '安全管理制度收发登记记录',
      '各类评审和修订记录（安全管理制度评审和修订记录、体系评审记录等）',
    ],
  },
  {
    name: 'table_1-18c',
    title: '表1-18 安全管理文档 - 安全管理机构',
    type: 'checklist',
    requirements: [
      '部门设置、岗位设置及工作职责定义方面的管理制度',
      '网络安全领导职责文件和最高领导的委任授权书',
      '机构安全管理人员岗位名单',
      '授权审批、审批流程等方面的管理制度',
      '各项审批和批准执行记录（来访人员进入机房审批、介质/设备外带审批、系统外联审批等）',
      '组织机构内部人员联系表',
      '外联单位联系列表',
      '各类会议纪要或记录（部门内、部门间协调会、领导小组、和外联单位之间）',
      '安全审核和安全检查方面的管理制度',
      '信息系统定期安全检查的检查表和安全检查报告',
    ],
  },
  {
    name: 'table_1-18d',
    title: '表1-18 安全管理文档 - 安全人员管理',
    type: 'checklist',
    requirements: [
      '人员录用、离岗、考核等方面的管理制度',
      '人员考核、审查、培训记录（人员录用、人员定期考核）、离岗手续',
      '人员保密协议',
      '关键岗位安全协议',
      '人员安全教育和培训方面的管理制度',
      '培训计划',
      '外部人员访问控制方面的管理制度',
      '外部人员访问重要区域（包括机房、受控网络、系统）的审批记录、登记记录',
      '外部人员签署的保密协议',
    ],
  },
  {
    name: 'table_1-18e',
    title: '表1-18 安全管理文档 - 安全建设管理',
    type: 'checklist',
    requirements: [
      '信息系统定级报告',
      '上级主管部门或本单位相关部门对信息系统定级结果的审批意见',
      '信息系统定级专家评审意见',
      '近期和远期安全建设工作计划、总体建设规划书',
      '详细设计方案',
      '总体安全策略等配套文件的专家论证文档',
      '产品选型、采购方面的管理制度',
      '产品的选型测试结果记录',
      '候选产品名单',
      '网络安全产品、密码产品符合有关规定的证明文档',
      '软件外包开发或自行软件开发方面的管理制度',
      '代码编写安全规范',
      '程序资源库修改、更新、发布的审批记录',
      '软件开发设计和用户指南等相关文档（目录体系框架或交还原型系统）、软件测试报告',
      '软件交付前的恶意代码检测报告',
      '软件源代码审查记录',
      '工程实施过程管理方面的管理制度',
      '工程实施方案',
      '第三方工程监理报告',
      '测试、验收方面的管理制度',
      '系统验收测试方案',
      '系统验收测试记录、报告，以及测试验收报告的审定文档',
      '系统交付清单',
      '系统建设文档（如系统建设方案）；指导用户进行系统运维的文档（如服务器操作规程书等）；系统培训手册等',
      '以往等级测评的测评报告和安全整改方案',
      '与安全服务商或外包开发商签订的服务合同和安全协议',
      '服务供应商定期提交的安全服务报告',
      '对服务供应商进行定期审核的报告',
      '服务供应商评价审核管理制度',
    ],
  },
  {
    name: 'table_1-18f',
    title: '表1-18 安全管理文档 - 安全运维管理',
    type: 'checklist',
    requirements: [
      '办公环境安全管理方面的管理制度',
      '资产、设备、介质安全管理方面的管理制度',
      '信息分类、标识、发布、使用方面的管理制度',
      '配套设施、软硬件维护方面的管理制度',
      '等级保护对象资产清单（含设备设施、软件、文档等）',
      '介质归档、查询等的登记记录',
      '维修和服务的审批、维修过程记录',
      '设备带离机房或办公地点的审批记录',
      '设备维护记录和主要设备操作日志',
      '网络和系统安全管理（网络配置、帐号管理等）方面的管理制度',
      '系统监控、风险评估、漏洞扫描方面的管理制度',
      '主机系统、网络、安全设备等的操作日志和维护记录',
      '识别安全漏洞和隐患的安全报告或记录',
      '安全测评报告',
      '网络或系统账户审批记录或流程',
      '重要设备或系统（如操作系统、数据库、网络设备、安全设备、应用和组件）的配置和操作手册',
      '运维操作日志',
      '系统运行日志、监测日志和报警数据等分析统计报告',
      '变更运维的审批记录',
      '变更运维的操作过程记录',
      '运维工具接入系统的审批记录',
      '运维工具的审计日志记录',
      '开通远程运维的审批记录',
      '系统相关人员网络外联（联网、合作伙伴企业网、上级部门网络）联的授权批准书',
      '配置信息记录',
      '配置信息的变更流程、更新记录',
      '病毒防范方面的管理制度',
      '恶意代码检测、升级记录和分析报告',
      '密码管理方面的管理制度',
      '国家密码管理主管部门规定的检测报告或密码产品型号证书',
      '系统变更控制方面的管理制度',
      '变更方案',
      '变更申请书',
      '变更方案评审记录和变更过程记录',
      '备份和恢复方面的管理制度',
      '数据备份和恢复策略文档',
      '定期备份的重要业务信息、系统数据、软件系统的列表或清单',
      '备份过程记录',
      '安全事件报告和处置方面的管理制度',
      '安全事件处理过程记录',
      '应急响应方法、应急响应计划等方面的文件',
      '应急预案培训、演练、审查记录',
      '外包运维服务单位的相关资质',
      '与外包运维服务单位签署的服务协议、服务合同',
    ],
  },

  // ── 表1-19: 安全服务 ──
  {
    name: 'table_1-19',
    title: '表1-19 安全服务',
    type: 'table',
    showHeader: true,
    defaultRows: 5,
    columns: [
      { prop: '安全服务名称', label: '安全服务名称', minWidth: 200 },
      { prop: '安全服务商', label: '安全服务商', minWidth: 200 },
    ],
    note: '安全服务包括系统集成、安全集成、安全运维、安全测评、应急响应、安全监测等所有相关安全服务。',
  },

  // ── 表1-20: 安全威胁情况调查 ──
  {
    name: 'table_1-20',
    title: '表1-20 安全威胁情况调查',
    type: 'form',
    showHeader: true,
    fields: [
      { key: '是否发生过网络安全事件', label: '是否发生过网络安全事件', type: 'radio', options: [
        { value: '没有', label: '没有' }, { value: '1次/年', label: '1次/年' },
        { value: '2次/年', label: '2次/年' }, { value: '3次以上/年', label: '3次以上/年' },
        { value: '不清楚', label: '不清楚' },
      ], span: 24 },
      { key: '安全事件说明', label: '安全事件说明（时间、影响）', type: 'textarea', rows: 2, span: 24 },
      { key: '发生的网络安全事件类型', label: '发生的网络安全事件类型', type: 'checkbox', options: [
        { value: '感染病毒/蠕虫/特洛伊木马程序', label: '感染病毒/蠕虫/特洛伊木马程序' },
        { value: '拒绝服务攻击', label: '拒绝服务攻击' },
        { value: '端口扫描攻击', label: '端口扫描攻击' },
        { value: '数据窃取', label: '数据窃取' },
        { value: '破坏数据或网络', label: '破坏数据或网络' },
        { value: '篡改网页', label: '篡改网页' },
        { value: '垃圾邮件', label: '垃圾邮件' },
        { value: '内部人员有意破坏', label: '内部人员有意破坏' },
        { value: '被利用发送和传播有害信息', label: '被利用发送和传播有害信息' },
        { value: '内部人员滥用网络端口、系统资源', label: '内部人员滥用网络端口、系统资源' },
        { value: '网络诈骗和盗窃', label: '网络诈骗和盗窃' },
        { value: '其他', label: '其他' },
      ], span: 24 },
      { key: '安全事件类型其他说明', label: '其他说明', span: 24 },
      { key: '如何发现网络安全事件', label: '如何发现网络安全事件', type: 'checkbox', options: [
        { value: '网络(系统)管理员工作监测发现', label: '网络(系统)管理员工作监测发现' },
        { value: '通过事后分析发现', label: '通过事后分析发现' },
        { value: '通过安全产品发现', label: '通过安全产品发现' },
        { value: '有关部门通知或意外发现', label: '有关部门通知或意外发现' },
        { value: '他人告知', label: '他人告知' },
        { value: '其他', label: '其他' },
      ], span: 24 },
      { key: '如何发现其他说明', label: '其他说明', span: 24 },
      { key: '网络安全事件造成损失评估', label: '网络安全事件造成损失评估', type: 'radio', options: [
        { value: '非常严重', label: '非常严重' }, { value: '严重', label: '严重' },
        { value: '一般', label: '一般' }, { value: '比较轻微', label: '比较轻微' },
        { value: '轻微', label: '轻微' }, { value: '无法评估', label: '无法评估' },
      ], span: 24 },
      { key: '可能的攻击来源', label: '可能的攻击来源', type: 'checkbox', options: [
        { value: '内部', label: '内部' }, { value: '外部', label: '外部' },
        { value: '都有', label: '都有' }, { value: '病毒', label: '病毒' },
        { value: '其他原因', label: '其他原因' }, { value: '不清楚', label: '不清楚' },
      ], span: 24 },
      { key: '攻击来源说明', label: '攻击来源说明', span: 24 },
      { key: '导致发生网络安全事件的可能原因', label: '导致发生网络安全事件的可能原因', type: 'checkbox', options: [
        { value: '未修补或防范软件漏洞', label: '未修补或防范软件漏洞' },
        { value: '网络或软件配置错误', label: '网络或软件配置错误' },
        { value: '登录密码过于简单或未修改', label: '登录密码过于简单或未修改' },
        { value: '缺少访问控制', label: '缺少访问控制' },
        { value: '攻击者使用拒绝服务攻击', label: '攻击者使用拒绝服务攻击' },
        { value: '攻击者利用软件默认设置', label: '攻击者利用软件默认设置' },
        { value: '利用内部用户安全管理漏洞或内部人员作案', label: '利用内部用户安全管理漏洞或内部人员作案' },
        { value: '内部网络违规连接互联网', label: '内部网络违规连接互联网' },
        { value: '攻击者使用欺诈方法', label: '攻击者使用欺诈方法' },
        { value: '不知原因', label: '不知原因' },
        { value: '其他', label: '其他' },
      ], span: 24 },
      { key: '可能原因其他说明', label: '其他说明', span: 24 },
      { key: '是否发生过硬件故障', label: '是否发生过硬件故障', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '硬件故障造成的影响', label: '造成的影响', span: 24 },
      { key: '是否发生过软件故障', label: '是否发生过软件故障', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '软件故障造成的影响', label: '造成的影响', span: 24 },
      { key: '是否发生过维护失误', label: '是否发生过维护失误', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '维护失误造成的影响', label: '造成的影响', span: 24 },
      { key: '是否发生过因用户操作失误引起的安全事件', label: '是否发生过因用户操作失误引起的安全事件', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '用户操作失误造成的影响', label: '造成的影响', span: 24 },
      { key: '是否发生过物理设施/设备被物理破坏', label: '是否发生过物理设施/设备被物理破坏', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '物理破坏造成的影响', label: '造成的影响', span: 24 },
      { key: '有无遭受自然性破坏', label: '有无遭受自然性破坏（如雷击等）', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '自然性破坏时间后果', label: '有请注明时间、事件后果', span: 24 },
      { key: '有无发生过莫名其妙的故障', label: '有无发生过莫名其妙的故障', type: 'radio', options: [
        { value: '有', label: '有(注明时间、频率)' }, { value: '无', label: '无' },
      ], span: 24 },
      { key: '莫名其妙的故障时间后果', label: '有请注明时间、事件后果', span: 24 },
    ],
  },
]
</script>

<style scoped>
.styled-collapse {
  border: none;
}

.styled-collapse :deep(.el-collapse-item) {
  margin-bottom: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: #fff;
  transition: box-shadow .15s;
}

.styled-collapse :deep(.el-collapse-item:hover) {
  box-shadow: var(--shadow-sm);
}

.styled-collapse :deep(.el-collapse-item__header) {
  height: 44px;
  padding: 0 16px;
  background: #fafbfc;
  border-bottom: 1px solid transparent;
  font-weight: 600;
  font-size: 14px;
  color: var(--text);
  transition: background .15s;
}

.styled-collapse :deep(.el-collapse-item__header:hover) {
  background: #f1f5f9;
}

.styled-collapse :deep(.el-collapse-item.is-active .el-collapse-item__header) {
  border-bottom-color: var(--border);
  background: #fff;
}

.styled-collapse :deep(.el-collapse-item__wrap) {
  border: none;
  background: #fff;
}

.styled-collapse :deep(.el-collapse-item__content) {
  padding: 12px;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.collapse-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 26px;
  padding: 0 6px;
  border-radius: 4px;
  background: var(--primary);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
  white-space: nowrap;
}
</style>
