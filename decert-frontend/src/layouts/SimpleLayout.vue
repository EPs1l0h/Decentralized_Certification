<!-- src/layouts/SimpleLayout.vue -->
<template>
  <div class="simple-layout">
    <router-view />
  </div>
</template>

<style scoped>
.simple-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}
</style>
