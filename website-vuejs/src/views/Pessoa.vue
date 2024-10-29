<template>
  <div class="container mx-auto pt-20 h-full">
    <h1 class="pg-about__title text-neutral-base text-4xl font-bold mb-10">
      Perfil
    </h1>
    <div class="grid grid-cols-7 gap-1">
      <div class="col-span-2">
        <user-info/>      
      </div>
      <div class="col-span-5">
        <user-perguntas/>
        <user-subscriptions/>
      </div>
    </div>
  </div>
</template>

<script>
import UserInfo from '@/components/user/UserInfo.vue'
import UserPerguntas from '@/components/user/UserPerguntas.vue'
import UserSubscriptions from '@/components/user/UserSubscriptions.vue'
export default {
  name: 'pessoa-view',
  components: {
    UserInfo,
    UserPerguntas,
    UserSubscriptions
  }
}
</script>
