// Assets are converted on build to base64 strings, so in Browser they can
// be used as variables, reducing request number.
export var assets = {
  logo: require('@/assets/images/logo.svg'),
  lupa: require('@/assets/icons/lupa.svg'),
  cc: require('@/assets/images/cc-by-nc-sa_icon.png'),
  planejado: require('@/assets/icons/mapa/planejado.svg'),
  empenhado: require('@/assets/icons/mapa/empenhado.svg'),
  liquidado: require('@/assets/icons/mapa/liquidado.svg'),
  aPla: require('@/assets/icons/atividades/planejado.svg'),
  aEmp: require('@/assets/icons/atividades/empenhado.svg'),
  aLiq: require('@/assets/icons/atividades/liquidado.svg'),
  aCom: require('@/assets/icons/atividades/comentarios.svg'),
  aComTop: require('@/assets/icons/atividades/comentarios-top.svg'),
  aComExtra: require('@/assets/icons/atividades/comentarios-extra.svg'),
  aPer: require('@/assets/icons/atividades/pergunta.svg'),
  // "isvg" is used to avoid default svg loader
  // eslint-disable-next-line
  moedas: require('svg-inline-loader!@/assets/icons/moedas.isvg'),
  patM: require('@/assets/icons/patM.png'),
  patNM: require('@/assets/icons/patNM.png')
}

export default function install (Vue) {
  Object.defineProperty(Vue.prototype, '$assets', {
    get () { return assets }
  })
}
