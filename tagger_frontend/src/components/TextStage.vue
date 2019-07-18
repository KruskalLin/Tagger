<template xmlns:v-contextmenu="http://www.w3.org/1999/xhtml">
  <div class="text-stage">
    <div class="title">Document: {{this.$store.getters.getFilename}}</div>
    <div class="sdc-article-body">
      <v-contextmenu ref="contextmenu">
        <v-contextmenu-item :disabled="disable" @click="deleteTags">delete</v-contextmenu-item>
      </v-contextmenu>
      <p v-html="showText" @contextmenu.prevent="over($event)"  v-contextmenu:contextmenu></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextStage',
  computed: {
    text: function () { return this.$store.getters.getText },
    tags: function () { return this.$store.getters.getTags },
    showText: function () {
      console.log(this.tags)
      let tags = this.tags
      let text = this.text
      let tempHtml = ''
      console.log(tempHtml)
      let lastend = 0
      for (let i = 0; i < tags.length; i++) {
        let start = tags[i].start
        let end = tags[i].end
        tempHtml += text.substring(lastend, start)
        tempHtml += '<span class="annotation" id="' + i + '">' + text.substring(start, end) + '</span>'
        lastend = end
      }
      tempHtml += text.substring(lastend)
      return tempHtml
    }
  },
  data () {
    return {
      disable: false,
      id: 0
    }
  },
  methods: {
    over: function (event) {
      if (event.target.nodeName === 'SPAN') {
        this.disable = false
        this.id = parseInt(event.target.id)
        return
      }
      this.disable = true
    },
    deleteTags () {
      let tags = this.$store.getters.getTags
      tags.splice(this.id, 1)
      this.$store.commit('setTags', tags)
    }
  }
}
</script>

<style scoped>
  .title{
    font-size: 30px;
    margin-bottom: 50px;
  }
  .sdc-article-body{
    font-family: times,serif;
    font-size: 20px;
    line-height:45px;
  }
  .text-stage{
    margin-left: 300px;
  }
  /deep/ .annotation {
    background-color: rgba(234, 2, 26, 0.1);
    text-decoration-skip-ink: none;
    cursor: move;
    position: relative;
    user-select: none;
  }
  /deep/ .annotation:hover {
    background-color: rgba(234, 2, 26, 0.3);
  }
</style>
