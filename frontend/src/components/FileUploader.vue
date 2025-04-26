<template>
  <div>
    <h2>Upload your TSV file</h2>
    
    <div>
      <input 
        type="file" 
        @change="onFileSelected" 
        accept=".tsv"
      />
      
      <button 
        @click="uploadFile" 
        :disabled="!fileToUpload"
      >
        Upload
      </button>
    </div>
    
    <div>
      <span>OR</span>
    </div>
    
    <h2>Select an existing file</h2>
    
    <div v-if="availableFiles.length === 0">
      No files available
    </div>
    
    <ul v-else>
      <li 
        v-for="file in availableFiles" 
        :key="file"
        @click="selectFile(file)"
      >
        {{ file }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

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
</script>
