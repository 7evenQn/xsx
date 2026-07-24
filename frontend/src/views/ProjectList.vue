<template>
  <div class="project-list-page">
    <!-- Welcome hero -->
    <div class="hero">
      <div class="hero-content">
        <h1>网络安全等级测评调研表</h1>
        <p>按照 GB/T 22239 标准，管理各单位信息系统安全等级保护测评填报工作</p>
      </div>
      <div class="hero-action">
        <el-button type="primary" size="large" @click="dialogVisible = true" round>
          + 新建项目
        </el-button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-num">{{ projects.length }}</div>
        <div class="stat-label">项目总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ todayCount }}</div>
        <div class="stat-label">今日更新</div>
      </div>
    </div>

    <!-- Project list -->
    <div class="section-head">
      <h2>项目列表</h2>
    </div>

    <div v-if="projects.length === 0" class="empty-state">
      <div class="empty-icon">&#128196;</div>
      <p>暂无项目，点击上方按钮新建</p>
    </div>

    <div v-else class="project-grid">
      <div
        v-for="p in projects"
        :key="p.id"
        class="project-card"
        @click="$router.push(`/project/${p.id}`)"
      >
        <div class="card-top">
          <div class="card-avatar">{{ (p.name || '?')[0] }}</div>
          <div class="card-info">
            <div class="card-title">{{ p.name }}</div>
            <div class="card-company">{{ p.company_name || '未设置单位' }}</div>
          </div>
        </div>
        <div class="card-meta">
          <span class="meta-tag">{{ p.system_name || '未设置系统' }}</span>
          <span class="meta-date">{{ p.updated_at?.split('T')[0] || '-' }}</span>
        </div>
        <div class="card-actions" @click.stop>
          <el-button size="small" text @click="$router.push(`/project/${p.id}`)">编辑</el-button>
          <el-button size="small" text type="danger" @click="confirmDelete(p)">删除</el-button>
        </div>
      </div>
    </div>

    <!-- Create dialog -->
    <el-dialog v-model="dialogVisible" title="新建项目" width="480px" :close-on-click-modal="false">
      <el-form :model="form" label-width="80px" label-position="top">
        <el-form-item label="项目名称">
          <el-input v-model="form.name" placeholder="例如：XX系统等保测评" size="large" />
        </el-form-item>
        <el-form-item label="单位名称">
          <el-input v-model="form.company_name" placeholder="被测评单位" size="large" />
        </el-form-item>
        <el-form-item label="系统名称">
          <el-input v-model="form.system_name" placeholder="被测评系统" size="large" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" size="large">取消</el-button>
        <el-button type="primary" @click="create" size="large">确定创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listProjects, createProject, deleteProject } from '../api/index.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const projects = ref([])
const dialogVisible = ref(false)
const form = ref({ name: '', company_name: '', system_name: '' })

const todayCount = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return projects.value.filter(p => p.updated_at?.startsWith(today)).length
})

onMounted(refresh)

async function refresh() {
  try {
    projects.value = await listProjects()
  } catch (e) {
    ElMessage.error('加载项目列表失败')
  }
}

async function create() {
  if (!form.value.name) { ElMessage.warning('请输入项目名称'); return }
  try {
    const p = await createProject(form.value)
    dialogVisible.value = false
    form.value = { name: '', company_name: '', system_name: '' }
    router.push(`/project/${p.id}`)
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

async function confirmDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除项目"${row.name}"吗？`, '确认删除', { type: 'warning' })
    await deleteProject(row.id)
    ElMessage.success('已删除')
    refresh()
  } catch (e) { /* cancelled */ }
}
</script>

<style scoped>
.project-list-page { max-width: 1200px; margin: 0 auto; }

.hero {
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
  border-radius: var(--radius-lg);
  padding: 40px 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.hero-content h1 {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.hero-content p {
  margin: 0;
  color: rgba(255,255,255,.75);
  font-size: 14px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  text-align: center;
}

.stat-num {
  font-size: 36px;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: 14px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-head h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-icon { font-size: 48px; margin-bottom: 12px; }

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

.project-card {
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: all .2s;
  border: 1px solid var(--border);
}

.project-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--primary);
}

.card-top {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-bottom: 14px;
}

.card-avatar {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.4;
}

.card-company {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.meta-tag {
  background: #eff6ff;
  color: #2563eb;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.meta-date {
  font-size: 12px;
  color: var(--text-muted);
}

.card-actions {
  border-top: 1px solid var(--border);
  padding-top: 12px;
  display: flex;
  gap: 8px;
}
</style>
