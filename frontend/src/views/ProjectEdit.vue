<template>
  <div class="project-edit">
    <!-- Toolbar -->
    <div class="edit-toolbar">
      <div class="toolbar-left">
        <el-button @click="$router.push('/')" text>
          <span style="font-size:16px;">&#8592;</span> 返回列表
        </el-button>
        <el-divider direction="vertical" />
        <div class="proj-badge">
          <span class="badge-dot"></span>
          {{ project.name || '未命名项目' }}
        </div>
      </div>
      <div class="toolbar-right">
        <el-button @click="saveAll" :loading="saving" type="primary" :icon="Check">
          保存
        </el-button>
        <el-button @click="downloadWord" type="success" plain>
          导出 Word
        </el-button>
        <el-button @click="downloadExcel" type="warning" plain>
          导出 Excel
        </el-button>
      </div>
    </div>

    <!-- Horizontal tab bar -->
    <div class="tabs-shell">
      <el-tabs v-model="activeTab" type="border-card" @tab-change="onTabChange" class="main-tabs">
        <el-tab-pane name="1">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">01</span>
              基本信息
            </span>
          </template>
          <BasicInfo ref="sec1Ref" v-model="sections[1]" />
        </el-tab-pane>

        <el-tab-pane name="2" :lazy="true">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">02</span>
              云计算
            </span>
          </template>
          <OptionalSection
            title="云计算应用情况"
            v-model:enabled="sectionEnabled[2]"
            v-model:data="sections[2]"
            ref="sec2Ref"
          >
            <CloudComputing v-model="sections[2]" />
          </OptionalSection>
        </el-tab-pane>

        <el-tab-pane name="3" :lazy="true">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">03</span>
              大数据
            </span>
          </template>
          <OptionalSection
            title="大数据应用情况"
            v-model:enabled="sectionEnabled[3]"
            v-model:data="sections[3]"
            ref="sec3Ref"
          >
            <BigData v-model="sections[3]" />
          </OptionalSection>
        </el-tab-pane>

        <el-tab-pane name="4" :lazy="true">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">04</span>
              工控系统
            </span>
          </template>
          <OptionalSection
            title="工业控制系统"
            v-model:enabled="sectionEnabled[4]"
            v-model:data="sections[4]"
            ref="sec4Ref"
          >
            <IndustrialCtrl v-model="sections[4]" />
          </OptionalSection>
        </el-tab-pane>

        <el-tab-pane name="5" :lazy="true">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">05</span>
              物联网
            </span>
          </template>
          <OptionalSection
            title="物联网系统"
            v-model:enabled="sectionEnabled[5]"
            v-model:data="sections[5]"
            ref="sec5Ref"
          >
            <IoT v-model="sections[5]" />
          </OptionalSection>
        </el-tab-pane>

        <el-tab-pane name="6" :lazy="true">
          <template #label>
            <span class="tab-label">
              <span class="tab-num">06</span>
              移动互联
            </span>
          </template>
          <OptionalSection
            title="移动互联系统"
            v-model:enabled="sectionEnabled[6]"
            v-model:data="sections[6]"
            ref="sec6Ref"
          >
            <MobileInter v-model="sections[6]" />
          </OptionalSection>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProject, saveSection, toggleSection, exportWord, exportExcel } from '../api/index.js'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import BasicInfo from './BasicInfo.vue'
import OptionalSection from '../components/OptionalSection.vue'
import CloudComputing from './CloudComputing.vue'
import BigData from './BigData.vue'
import IndustrialCtrl from './IndustrialCtrl.vue'
import IoT from './IoT.vue'
import MobileInter from './MobileInter.vue'

const route = useRoute()
const projectId = Number(route.params.id)
const project = ref({ name: '' })
const activeTab = ref('1')
const saving = ref(false)

const sections = reactive({ 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{} })
const sectionEnabled = reactive({ 2:false, 3:false, 4:false, 5:false, 6:false })

const sec1Ref = ref(null)
const sec2Ref = ref(null)
const sec3Ref = ref(null)
const sec4Ref = ref(null)
const sec5Ref = ref(null)
const sec6Ref = ref(null)

onMounted(async () => {
  try {
    const p = await getProject(projectId)
    project.value = p
    sections[1] = p.section1_data || {}
    sections[2] = p.section2_data || {}
    sections[3] = p.section3_data || {}
    sections[4] = p.section4_data || {}
    sections[5] = p.section5_data || {}
    sections[6] = p.section6_data || {}
    sectionEnabled[2] = p.section2_enabled
    sectionEnabled[3] = p.section3_enabled
    sectionEnabled[4] = p.section4_enabled
    sectionEnabled[5] = p.section5_enabled
    sectionEnabled[6] = p.section6_enabled
  } catch (e) {
    ElMessage.error('加载项目失败')
  }
})

function getSectionData(secNum) {
  const refMap = { 1: sec1Ref, 2: sec2Ref, 3: sec3Ref, 4: sec4Ref, 5: sec5Ref, 6: sec6Ref }
  return refMap[secNum]?.value?.getData?.() || sections[secNum] || {}
}

async function onTabChange() { await saveCurrentSection() }

async function saveCurrentSection() {
  const num = Number(activeTab.value)
  const data = getSectionData(num)
  sections[num] = data
  try { await saveSection(projectId, num, data) } catch (e) {}
}

async function saveAll() {
  saving.value = true
  try {
    const num = Number(activeTab.value)
    sections[num] = getSectionData(num)
    await saveSection(projectId, num, sections[num])
    for (let i = 2; i <= 6; i++) await toggleSection(projectId, i, sectionEnabled[i])
    ElMessage.success('保存成功')
  } catch (e) { ElMessage.error('保存失败') }
  saving.value = false
}

function downloadWord() { window.open(exportWord(projectId)) }
function downloadExcel() { window.open(exportExcel(projectId)) }
</script>

<style scoped>
.project-edit { max-width: 1300px; margin: 0 auto; }

.edit-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  margin-bottom: 20px;
  position: sticky;
  top: 72px;
  z-index: 100;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.proj-badge {
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}

.tabs-shell {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.main-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
  background: #f8fafc;
  border-bottom: 1px solid var(--border);
}

.main-tabs :deep(.el-tabs__nav-wrap) {
  overflow-x: auto;
}

.main-tabs :deep(.el-tabs__nav) {
  display: flex;
  flex-wrap: nowrap;
}

.main-tabs :deep(.el-tabs__content) {
  padding: 16px 20px 20px;
}

.main-tabs :deep(.el-tabs__item) {
  height: 44px;
  line-height: 44px;
  font-size: 13px;
  font-weight: 500;
  padding: 0 20px;
  border-right: 1px solid var(--border);
  flex-shrink: 0;
}

.main-tabs :deep(.el-tabs__item:last-child) {
  border-right: none;
}

.main-tabs :deep(.el-tabs__item.is-active) {
  background: #fff;
  color: var(--primary);
  font-weight: 600;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
}

.tab-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #e8f0fe;
  color: var(--primary);
  font-size: 12px;
  font-weight: 700;
}
</style>
