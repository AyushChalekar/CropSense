<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import Navbar from '../components/ui/Navbar.vue';

// --- Types ---
interface PredictionData {
  // General
  hectares: number; agriblock: string; variety: string; soilType: string;
  seedRate: number; lpMainfield: number; nursery: string; nurseryArea: number; lpNursery: number;
  
  // Nutrients & Care
  dap20Days: number; weed28Days: number; urea40Days: number; 
  potash50Days: number; micro70Days: number; pest60Days: number;
  
  // Weather (Simplified grouping for the sake of the UI demo)
  rain30Days: number; rain30to50: number; rain51to70: number; rain71to105: number;
  // ... (In a real app, you'd map every single specific weather field here)
}

// --- State ---
const currentStage = ref(1); // 1: Input, 2: Processing, 3: Result
const isProcessing = ref(false);
const showOcrModal = ref(false);

// Reactive form data
const formData = reactive<PredictionData>({
  hectares: 0, agriblock: '', variety: '', soilType: '',
  seedRate: 0, lpMainfield: 0, nursery: '', nurseryArea: 0, lpNursery: 0,
  dap20Days: 0, weed28Days: 0, urea40Days: 0, potash50Days: 0, micro70Days: 0, pest60Days: 0,
  rain30Days: 0, rain30to50: 0, rain51to70: 0, rain71to105: 0
});

// Mock Result Data
const predictionResult = reactive({
  yield: 0,
  accuracy: 0,
  grade: ''
});

// --- Actions ---

const triggerOCR = () => {
  // Placeholder for Optical Character Recognition logic
  showOcrModal.value = true;
  setTimeout(() => {
    showOcrModal.value = false;
    // Simulate data filling
    formData.hectares = 2.5;
    formData.soilType = 'Alluvial';
    formData.variety = 'CR-1009';
    alert("OCR Scan Complete: Data auto-filled!");
  }, 1500);
};

const submitPrediction = () => {
  currentStage.value = 2;
  isProcessing.value = true;

  // Simulate ML Model API Call
  setTimeout(() => {
    isProcessing.value = false;
    currentStage.value = 3;
    
    // Mock Logic for result
    predictionResult.yield = 4500 + (Math.random() * 500); // Random yield between 4.5 - 5.0 tons
    predictionResult.accuracy = 94.2;
    predictionResult.grade = 'A+';
  }, 3000); // 3 second delay for "Processing"
};

const resetForm = () => {
  currentStage.value = 1;
  // Optional: Reset formData here
};
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-inter">
    <Navbar />

    <div class="max-w-5xl mx-auto px-4 py-8">
      
      <div class="flex justify-center mb-8">
        <div class="flex items-center space-x-4">
          <div :class="`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-colors ${currentStage >= 1 ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-500'}`">1</div>
          <div class="w-16 h-1 bg-gray-200"><div :class="`h-full bg-green-600 transition-all duration-500 ${currentStage >= 2 ? 'w-full' : 'w-0'}`"></div></div>
          <div :class="`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-colors ${currentStage >= 2 ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-500'}`">2</div>
          <div class="w-16 h-1 bg-gray-200"><div :class="`h-full bg-green-600 transition-all duration-500 ${currentStage >= 3 ? 'w-full' : 'w-0'}`"></div></div>
          <div :class="`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-colors ${currentStage >= 3 ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-500'}`">3</div>
        </div>
      </div>

      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 1" class="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-slate-800">Crop Parameters</h2>
            <button @click="triggerOCR" class="flex items-center gap-2 bg-blue-50 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors">
              <span class="text-xl">📷</span> Auto-fill with OCR
            </button>
          </div>

          <form @submit.prevent="submitPrediction" class="space-y-8">
            
            <div class="bg-slate-50 p-6 rounded-lg">
              <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b border-gray-200 pb-2">🌾 Field Information</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Hectares</label>
                  <input v-model="formData.hectares" type="number" step="0.1" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Variety</label>
                  <input v-model="formData.variety" type="text" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Soil Type</label>
                  <select v-model="formData.soilType" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                    <option>Clay</option>
                    <option>Alluvial</option>
                    <option>Loam</option>
                    <option>Sandy</option>
                  </select>
                </div>
                </div>
            </div>

            <div class="bg-slate-50 p-6 rounded-lg">
              <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b border-gray-200 pb-2">🧪 Fertilizers & Care</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Urea (40 Days)</label>
                  <input v-model="formData.urea40Days" type="number" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">DAP (20 Days)</label>
                  <input v-model="formData.dap20Days" type="number" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
                </div>
            </div>

             <div class="bg-slate-50 p-6 rounded-lg">
              <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b border-gray-200 pb-2">🌦️ Weather Conditions</h3>
              <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                 <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Rain (30D)</label>
                  <input v-model="formData.rain30Days" type="number" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
                 <div>
                  <label class="block text-sm font-medium text-slate-600 mb-1">Rain (30-50D)</label>
                  <input v-model="formData.rain30to50" type="number" class="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border">
                </div>
              </div>
            </div>

            <div class="flex justify-end pt-4">
              <button type="submit" class="bg-green-600 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:bg-green-700 transform transition hover:-translate-y-0.5">
                Calculate Yield Prediction
              </button>
            </div>
          </form>
        </div>
      </transition>

      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 2" class="flex flex-col items-center justify-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="relative w-24 h-24 mb-8">
            <div class="absolute top-0 left-0 w-full h-full border-4 border-green-100 rounded-full"></div>
            <div class="absolute top-0 left-0 w-full h-full border-4 border-green-600 rounded-full animate-spin border-t-transparent"></div>
          </div>
          <h3 class="text-2xl font-bold text-slate-800 mb-2">Analyzing Crop Data...</h3>
          <p class="text-slate-500 animate-pulse">Running XGBoost Regression Model</p>
        </div>
      </transition>

      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 3" class="bg-white rounded-xl shadow-lg border border-green-100 overflow-hidden">
          <div class="bg-green-600 p-8 text-center text-white">
            <h2 class="text-3xl font-bold mb-2">Prediction Complete</h2>
            <p class="opacity-90">Based on your inputs, here is the forecasted harvest.</p>
          </div>
          
          <div class="p-8">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div class="bg-green-50 rounded-xl p-6 border border-green-200 text-center">
                <span class="block text-green-800 font-semibold mb-2">Estimated Yield</span>
                <span class="block text-5xl font-bold text-green-700 mb-2">{{ Math.round(predictionResult.yield) }} <span class="text-2xl">Kg</span></span>
                <span class="text-sm text-green-600">Per Hectare</span>
              </div>
              
              <div class="bg-blue-50 rounded-xl p-6 border border-blue-200">
                <h4 class="font-bold text-blue-900 mb-4">Model Analytics</h4>
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-blue-700">Confidence Score</span>
                    <span class="font-bold text-blue-900">{{ predictionResult.accuracy }}%</span>
                  </div>
                  <div class="w-full bg-blue-200 h-2 rounded-full overflow-hidden">
                    <div class="bg-blue-600 h-full" style="width: 94%"></div>
                  </div>
                  <div class="pt-2 text-sm text-blue-800 leading-relaxed">
                    This forecast uses historical data from your Agriblock. Soil moisture was the dominant factor in this calculation.
                  </div>
                </div>
              </div>
            </div>

            <div class="flex justify-center gap-4">
              <button @click="resetForm" class="border border-slate-300 text-slate-600 px-6 py-2 rounded-lg hover:bg-slate-50 font-medium">
                Make Another Prediction
              </button>
              <button class="bg-slate-800 text-white px-6 py-2 rounded-lg hover:bg-slate-900 font-medium flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Save to History
              </button>
            </div>
          </div>
        </div>
      </transition>

    </div>

    <div v-if="showOcrModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
      <div class="bg-white p-8 rounded-xl shadow-2xl max-w-sm w-full text-center">
        <div class="animate-pulse mb-4 text-4xl">📷</div>
        <h3 class="text-xl font-bold mb-2">Scanning Document...</h3>
        <p class="text-gray-500">Extracting parameters from uploaded Soil Health Card.</p>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* Smooth fade transitions between stages */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>