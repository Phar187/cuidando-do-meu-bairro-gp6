<template>
  <div class="c-despesa-details">
    <div class="c-despesa-details__orgao pt-5 border-t-2 mt-10">
        <!-- <span class="block-decorator"/> falta icone -->
        <p class="text-neutral-base font-semibold">{{ $t('Accountable body') }}</p>
        <p class="text-neutral-light">{{ pointInfo.ds_orgao }}</p>
    </div>

    <ul class="list-bare top-bar bottom-bar despesa-details-list">
        <li v-for="el of mainKeys" :key="el[0]" class="my-5">
            <p class="text-neutral-base font-semibold">{{ el[0] }}</p>
            <p class="text-neutral-light">{{ el[1] }}</p>
        </li>

        <li v-for="empenho of empenhos" :key="empenho.codEmpenho">
          <a :href="'http://sfemp.prefeitura.sp.gov.br/extrato_empenho.aspx?Empenho=' + empenho.codEmpenho + '&Ano=' + empenho.anoEmpenho" target="_blank">Nota de empenho</a>
        </li>
    </ul>

    <div class="c-despesa-details__infos">
        <p class="text-neutral-base font-semibold">Licitações</p>
        <p class="text-neutral-light mb-3">Quer saber mais sobre o processo de licitações desta despesa?</p>
        <a class=" text-secondary-base underline" href="http://e-negocioscidadesp.prefeitura.sp.gov.br/BuscaLicitacao.aspx" target="_blank">Pesquise licitações</a>
        
        <p class="text-neutral-base font-semibold mt-8">Contratos</p>
         <p class="text-neutral-light mb-3">Quer saber mais sobre o processo de contratos desta despesa?</p>
        <a class="text-secondary-base underline" href="http://transparencia.prefeitura.sp.gov.br/contratos-convenios-e-compras-publicas/#tipo" target="_blank">Pesquise contratos</a>
        
    </div>
    <div class="c-despesa-details__code-information my-10">
      <h3 class="text-neutral-base font-semibold text-xl">Mais informações</h3>
      <p class="text-neutral-light mb-3">Aqui estão todas as informações mapeadas sobre essa despesa em formato JSON</p>
      <button v-if="!showAllInfo"
          class="bg-secondary-light text-white py-2 px-3 rounded font-light hover:bg-secondary-base"
          @click="showAllInfo = true">
          Mais informações
      </button>
      <button v-else
        class="bg-secondary-light text-white py-2 px-3 rounded font-light hover:bg-secondary-base"
        @click="showAllInfo = false">
        Esconder informações
      </button>
      <div id="resultCode" class="mt-10" v-if="showAllInfo && pointInfo">
        <code-highlight language="json">
          {
          <pre v-for="key of keys" :key="key">
            "{{ key }}": "{{ pointInfo[key] }}"
          </pre>
          }
        </code-highlight>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import CodeHighlight from "vue-code-highlight/src/CodeHighlight.vue";
import "vue-code-highlight/themes/prism.css";
import 'prism-es6/components/prism-json';

export default {
  name: 'despesa-details',
  data () {
    return {
      showAllInfo: false
    }
  },
  computed: {
    mainKeys () {
      let mainKeysNames = [
        ['ds_despesa', 'Despesa'],
        ['ds_fonte', 'Fonte'],
        ['ds_funcao', 'Função']
      ]
      let mainKeys = []
      for (let name of mainKeysNames) {
        let value = this.pointInfo[name[0]]
        if (value) mainKeys.push([name[1], value])
      }
      return mainKeys
    },
    keys () { return Object.keys(this.pointInfo) },
    ...mapState({
      pointInfo: state => state.money.pointInfo,
      empenhos: state => state.empenhos.empenhos
    })
  },
  methods: {
  },
  components: {
    CodeHighlight,
  }
}
</script>
