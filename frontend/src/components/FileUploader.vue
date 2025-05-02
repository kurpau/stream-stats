<template>
  <div class="card card-border w-96">
    <div class="card-body">
      <h2 class="card-title">Upload your TSV file</h2>

      <div>
        <input 
          type="file" 
          @change="onFileSelected" 
          accept=".tsv"
          class="file-input mb-2"
        />

        <button 
          @click="uploadFile" 
          :disabled="!fileToUpload"
          class="btn btn-primary"
        >
          Upload
        </button>
      </div>

      <div class="divider">OR</div>

      <h2 class="card-title">Select an existing file</h2>

      <div v-if="availableFiles.length === 0">
        No files available
      </div>

      <ul v-else class="menu bg-base-200 rounded-box w-full">
        <li 
          v-for="file in sortedFiles" 
          :key="file"
          @click="selectFile(file)"
        >
          <a>{{ file }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  availableFiles: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['file-selected', 'file-uploaded'])

const fileToUpload = ref(null)
const apiUrl = 'http://localhost:8000'

const onFileSelected = (event) => {
  fileToUpload.value = event.target.files[0]
}

const uploadFile = async () => {
  if (!fileToUpload.value) return
  
  const formData = new FormData()
  formData.append('file', fileToUpload.value)
  
  try {
    const response = await fetch(`${apiUrl}/upload-tsv/`, {
      method: 'POST',
      body: formData
    })
    
    const result = await response.json()
    if (response.ok) {
      emit('file-uploaded', result.filename)
    } else {
      alert(`Upload failed: ${result.detail}`)
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    alert('Error uploading file. Make sure the backend server is running.')
  }
}

const selectFile = (filename) => {
  emit('file-selected', filename)
}

const sortedFiles = computed(() => {
  return [...props.availableFiles].sort().reverse()
})
</script>
