<template>
  <div class="sidebar">
    <div>Tips:</div>
    <div style="font-size: 15px; color: #797979;margin-bottom: 20px;margin-top: 10px;">不支持含非utf-8字符文件<br>
    利用Stanford NER CRF训练的模型<br>
    英文LOCATION NER<br>
    上传文件即有标注，手动标注删除导出</div>
    <el-button size="small" type="success" @click="exportFile">Export</el-button>
    <el-button size="small" type="danger" @click="saveTags">Save</el-button>
    <el-button type="warning" icon="el-icon-edit" @click="tag" circle></el-button>
    <el-upload
      class="upload"
      :action="this.URL.uploads"
      :on-remove.sync="remove"
      :on-preview.sync="preview"
      :on-success.sync="success"
      :on-error="this.$message.error('non-utf8 character contain!!!')"
      :file-list="fileList">
      <el-button size="small" type="primary">Upload</el-button>
      <div slot="tip" class="el-upload__tip">Only txt file whose size is less than 16MB</div>
    </el-upload>
  </div>
</template>

<script>
import FileSaver from 'file-saver'

export default {
  name: 'UploadTexts',
  data () {
    return {
      fileList: []
    }
  },
  mounted () {
    this.fetchList()
  },
  methods: {
    async success (response, file, fileList) {
      let filename = response.url.substring(response.url.lastIndexOf('=') + 1)
      let date = filename.substring(filename.lastIndexOf('%24') + 3)
      let prefix = filename.substring(0, filename.lastIndexOf('%24'))
      await this.$axios.get(this.URL.getTags,
        {
          params: {
            name: prefix + '$' + date
          }
        }).then(res => {
        this.$store.commit('setTags', res.data.data)
      })
        .catch(error => {
          console.log(error)
        })
      await this.$axios.get(this.URL.getTexts,
        {
          params: {
            name: prefix + '$' + date
          }
        }).then(res => {
        this.$store.commit('setFilename', prefix + date.substring(date.lastIndexOf('.')))
        this.$store.commit('setRealName', prefix + '$' + date)
        this.$store.commit('setText', res.data)
      })
        .catch(error => {
          console.log(error)
        })
    },
    async preview (file) {
      if (file.response) {
        return
      }
      await this.$axios.get(this.URL.getTags,
        {
          params: {
            name: file.realName
          }
        }).then(res => {
        this.$store.commit('setTags', res.data.data)
      })
        .catch(error => {
          console.log(error)
        })
      await this.$axios.get(this.URL.getTexts,
        {
          params: {
            name: file.realName
          }
        }).then(res => {
        this.$store.commit('setFilename', file.realName.substring(0, file.realName.lastIndexOf('$')) + file.realName.substring(file.realName.lastIndexOf('.')))
        this.$store.commit('setRealName', file.realName)
        this.$store.commit('setText', res.data)
      })
        .catch(error => {
          console.log(error)
        })
    },
    async remove (file, fileList) {
      await this.$axios.get(this.URL.deleteFile,
        {
          params: {
            name: file.realName
          }
        }).then(res => {
        console.log(res)
      })
        .catch(error => {
          console.log(error)
        })
    },
    async fetchList () {
      return this.$axios.get(this.URL.getTextList)
        .then(res => {
          this.fileList = res.data.list.map(item => {
            return {
              name: item.substring(0, item.lastIndexOf('$')) + item.substring(item.lastIndexOf('.')),
              realName: item
            }
          })
        })
        .catch(error => {
          console.log(error)
        })
    },
    tag () {
      if (this.$store.getters.getFilename === '') {
        return
      }
      if (window.getSelection().baseNode.parentElement.tagName === 'P') {
        let tags = this.$store.getters.getTags
        let start = window.getSelection().anchorOffset
        let end = window.getSelection().focusOffset
        let word = window.getSelection().baseNode.data.substring(start, end)
        if (window.getSelection().baseNode.previousElementSibling && window.getSelection().baseNode.previousElementSibling.tagName === 'SPAN') {
          let tagId = parseInt(window.getSelection().baseNode.previousElementSibling.id)
          let tag = tags[tagId]
          tags.splice(tagId + 1, 0,
            {
              'start': tag.end + start,
              'end': tag.end + end,
              'word': word
            }
          )
          this.$store.commit('setTags', tags)
        } else {
          tags.splice(0, 0,
            {
              'start': start,
              'end': end,
              'word': word
            }
          )
          this.$store.commit('setTags', tags)
        }
      }
    },
    saveTags () {
      if (this.$store.getters.getFilename === '') {
        return
      }
      this.$axios.post(this.URL.saveTags,
        { 'name': this.$store.getters.getRealName,
          'tags': this.$store.getters.getTags}
      ).then(res => {
      })
        .catch(error => {
          console.log(error)
        })
    },
    exportFile () {
      if (this.$store.getters.getFilename === '') {
        return
      }
      const data = JSON.stringify({ 'data': this.$store.getters.getTags })
      const blob = new Blob([data], {type: ''})
      FileSaver.saveAs(blob, 'data.json')
    }
  }
}
</script>

<style scoped>
  .sidebar{
    float: left;
    position: fixed;
    margin-top: 20px;
  }
  .upload{
    margin-top: 20px;
  }
</style>
