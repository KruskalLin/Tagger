<template>
  <div id="app">
    <UploadTexts/>
    <TextStage/>
  </div>
</template>

<script>
import TextStage from './components/TextStage'
import UploadTexts from './components/UploadTexts'

export default {
  name: 'App',
  components: {
    TextStage,
    UploadTexts
  }
}
</script>

<style>
#app {
  justify-content: center;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 100px;
}
</style>
