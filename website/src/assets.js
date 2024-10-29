// Assets are converted on build to base64 strings, so in Browser they can
// be used as variables, reducing request number.
const assets = {
    logo: require('url?once=1!../assets/logo.svg'),
    lupa: require('url?once=1!../assets/lupa.svg'),
    planejado: require('url?once=1!../assets/map/planejado.svg'),
    empenhado: require('url?once=1!../assets/map/empenhado.svg'),
    liquidado: require('url?once=1!../assets/map/liquidado.svg'),
    aPla: require('url?once=1!../assets/activities/planejado.svg'),
    aEmp: require('url?once=1!../assets/activities/empenhado.svg'),
    aLiq: require('url?once=1!../assets/activities/liquidado.svg'),
    aCom: require('url?once=1!../assets/activities/comments.svg'),
    aComTop: require('url?once=1!../assets/activities/comments-top.svg'),
    aComExtra: require('url?once=1!../assets/activities/comments-extra.svg'),
    aPer: require('url?once=1!../assets/activities/pergunta.svg'),
    moedas: require('raw!../assets/moedas.svg'),
    patM: require('url?once=1!../assets/patM.png'),
    patNM: require('url?once=1!../assets/patNM.png'),
}

export default assets
