import Vapi from 'vuex-rest-api'
import { baseUrls } from '@/configs'
import { httpNoHeaders } from '@/utils'

// Empenhos Prefeitura
export default new Vapi({
  axios: httpNoHeaders,
  baseURL: baseUrls.empenhos,
  state: {
    empenhos: []
  }
}).get({
  headers: {
    Authorization: 'Bearer 198f959a5f39a1c441c7c863423264'
  },
  action: 'getEmpenhos',
  property: 'empenhos',
  path ({ pointInfo }) {
    let filters = {
      anoEmpenho: 'cd_exercicio',
      codOrgao: 'cd_orgao',
      codModalidade: 'cd_modalidade',
      codFuncao: 'cd_funcao',
      codSubFuncao: 'cd_subfuncao',
      codProjetoAtividade: 'projetoatividade',
      codPrograma: 'cd_programa',
      codElemento: 'cd_elemento',
      codFonteRecurso: 'cd_fonte',
      codCategoria: 'categoria_despesa',
      codGrupo: 'grupo_despesa'
    }
    return 'consultaEmpenhos?mesEmpenho=12&' +
      Object.keys(filters).map(k => k + '=' + pointInfo[filters[k]]).join('&')
  },
  onSuccess: (state, payload, axios) => {
    state.empenhos = payload.data.lstEmpenhos
  }
}).getStore()
