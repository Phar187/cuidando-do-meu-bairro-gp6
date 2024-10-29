<template>
  <div id="app">
    <main-menu />
    <div class="content pt-16">
      <transition name="fade" mode="out-in">
        <keep-alive>
            <!-- <router-view name="map"></router-view> -->
            <map-despesas v-if="routeName === 'despesa' || routeName === 'home'"/>
        </keep-alive>
      </transition>
      <transition name="fade" mode="out-in">
            <!-- <keep-alive> -->
          <router-view>
                <!-- <router-view name="map"></router-view> -->
                <!-- <map-despesas/> -->
          </router-view>
            <!-- </keep-alive> -->
      </transition>
      <msg-shower/>
    </div>
    <footer-info />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import MainMenu from '@/components/MainMenu.vue'
import MsgShower from '@/components/MsgShower.vue'
import MapDespesas from '@/components/MapDespesas.vue'
import FooterInfo from './components/FooterInfo.vue'

export default {
  components: {
    MainMenu,
    MsgShower,
    MapDespesas,
    FooterInfo
  },
  computed: {
    ...mapState({
      routeName: state => state.route.name,
      year: state => state.route.params.year,
      code: state => state.route.params.code,
      page: state => state.route.params.page,
      username: state => state.auth.username,
      pointInfo: state => state.money.pointInfo,
      viewingUser: state => state.route.params.viewingUser
    })
  },
  mounted () {
    this.loadPrevAuthData()
  },
  methods: {
    ...mapActions([
      'getYearPoints',
      'getYearInfo',
      'getPointInfo',
      'getEmpenhos',
      'getMoneyPage',
      'getPedidos',
      'getComments',
      'getUserInfo',
      'getMyUserInfo',
      'getUserPerguntas',
      'getSubscriptions',
      'loadPrevAuthData'
    ])
  },
  watch: {
    year: {
      handler (newValue, oldValue) {
        if (newValue) {
          this.getYearPoints({ params: { year: newValue } })
          this.getYearInfo({ params: { year: newValue } })
        }
      },
      immediate: true
    },
    code: {
      handler (newValue, oldValue) {
        if (newValue) {
          this.getPointInfo({ params: { code: newValue } })
          this.getPedidos({ params: { key: newValue } })
          this.getComments({ params: { key: newValue } })
        }
      },
      immediate: true
    },
    viewingUser: {
      handler (newValue, oldValue) {
        if (newValue) {
          this.getUserPerguntas({ params: { username: newValue } })
          if (newValue === this.username) {
            this.getMyUserInfo({ params: { username: newValue } })
          } else {
            this.getUserInfo({ params: { username: newValue } })
          }
        }
      },
      immediate: true
    },
    username: {
      handler (newValue, oldValue) {
        if (newValue) {
          this.getSubscriptions()
          if (newValue === this.viewingUser) {
            this.getMyUserInfo({ params: { username: newValue } })
          }
          // TODO else limpar userInfo? mas quando? não é sempre...
        }
      },
      immediate: true
    },
    page: {
      handler (newValue, oldValue) {
        if (newValue) this.getMoneyPage({ params: { year: this.year, page: newValue } })
      },
      immediate: true
    },
    pointInfo (newValue, oldValue) {
      if (newValue) this.getEmpenhos({ params: { pointInfo: newValue } })
    }
  }
}
</script>

<style lang="scss">
.fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}
.content {
  min-height: 100%;
  margin-bottom: -5rem;
}
</style>
