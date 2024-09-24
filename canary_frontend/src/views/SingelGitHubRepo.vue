<template>
  <div>
    <h1>Repository Details</h1>
    <form @submit.prevent="selectRepository">
      <div class="form-group">
        <label for="repoName">Repository Name:</label>
        <input type="text" id="repoName" v-model="repoName" required>
      </div>
      <div class="form-group">
        <label for="repoUrl">Repository URL:</label>
        <input type="url" id="repoUrl" v-model="repoUrl" required>
      </div>
      <button type="submit">Select Repository</button>
    </form>
    <div v-if="repoEvents.length">
      <h2>Repository Events</h2>
      <ul>
        <li v-for="event in repoEvents" :key="event.id">
          <span v-if="event.event_type === 'push'">
            Push Event: {{ event.message }} by {{ event.author }}
          </span>
          <span v-else-if="event.event_type === 'pull_request'">
            Pull Request Event: {{ event.message }} by {{ event.author }} ({{ event.url }})
          </span>
          <span v-else-if="event.event_type === 'pull_request_merged'">
            Pull Request Merged Event: {{ event.message }} by {{ event.author }} ({{ event.url }})
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      repoName: '',
      repoUrl: '',
      repoEvents: []
    }
  },
  methods: {
    selectRepository() {
      const repoData = {
        repo_name: this.repoName,
        repo_url: this.repoUrl
      }
      this.$axios.post('/api/select-repo/', repoData)
        .then(response => {
          console.log(response.data)
          // Fetch repository events
          this.$axios.get(`/api/repo-events/${this.repoName}`)
            .then(response => {
              this.repoEvents = response.data
            })
            .catch(error => {
              console.error(error)
            })
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>