import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export function listProjects() {
  return api.get('/projects').then(r => r.data)
}

export function createProject(data) {
  return api.post('/projects', data).then(r => r.data)
}

export function getProject(id) {
  return api.get(`/projects/${id}`).then(r => r.data)
}

export function updateProject(id, data) {
  return api.put(`/projects/${id}`, data).then(r => r.data)
}

export function deleteProject(id) {
  return api.delete(`/projects/${id}`).then(r => r.data)
}

export function saveSection(projId, sectionNum, data) {
  return api.put(`/projects/${projId}/section`, { section_num: sectionNum, data }).then(r => r.data)
}

export function toggleSection(projId, sectionNum, enabled) {
  return api.put(`/projects/${projId}/section/enable`, { section_num: sectionNum, enabled }).then(r => r.data)
}

export function exportWord(projId) {
  return `/api/projects/${projId}/export/word`
}

export function exportExcel(projId) {
  return `/api/projects/${projId}/export/excel`
}
