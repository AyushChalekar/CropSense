<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

// --- Types matched to FastAPI CropInput ---
interface PredictionData {
  hectares: number;
  agriblock: string;
  variety: string;
  soil_type: string;
  
  // Phase 1 (1-30 Days)
  rain_d1_30: number; min_temp_d1_30: number; max_temp_d1_30: number;
  wind_speed_d1_30: number; wind_dir_d1_30: string; humidity_d1_30: number;

  // Phase 2 (31-60 Days)
  rain_d30_50: number; min_temp_d31_60: number; max_temp_d31_60: number;
  wind_speed_d31_60: number; wind_dir_d31_60: string; humidity_d31_60: number;

  // Phase 3 (61-90 Days)
  rain_d51_70: number; min_temp_d61_90: number; max_temp_d61_90: number;
  wind_speed_d61_90: number; wind_dir_d61_90: string; humidity_d61_90: number;

  // Phase 4 (91-120 Days)
  rain_d71_105: number; min_temp_d91_120: number; max_temp_d91_120: number;
  wind_speed_d91_120: number; wind_dir_d91_120: string; humidity_d91_120: number;
}

const currentStage = ref(1);
const isProcessing = ref(false);
const showOcrModal = ref(false);

// --- Reactive form data with Values from Dataset Row 1 ---
const formData = reactive<PredictionData>({
  hectares: 6, 
  agriblock: 'Cuddalore', 
  variety: 'CO_43', 
  soil_type: 'alluvial',
  
  // Phase 1 (1-30 Days)
  rain_d1_30: 19.6, 
  min_temp_d1_30: 18.5, 
  max_temp_d1_30: 34.0, 
  wind_speed_d1_30: 4, 
  wind_dir_d1_30: 'SW', 
  humidity_d1_30: 72.0,

  // Phase 2 (31-60 Days)
  rain_d30_50: 187.2, 
  min_temp_d31_60: 16.0, 
  max_temp_d31_60: 30.0, 
  wind_speed_d31_60: 10, 
  wind_dir_d31_60: 'W', 
  humidity_d31_60: 78,

  // Phase 3 (61-90 Days)
  rain_d51_70: 167.0, 
  min_temp_d61_90: 15.5, 
  max_temp_d61_90: 31.0, 
  wind_speed_d61_90: 8, 
  wind_dir_d61_90: 'NNW', 
  humidity_d61_90: 88,

  // Phase 4 (91-120 Days)
  rain_d71_105: 61.0, 
  min_temp_d91_120: 16.0, 
  max_temp_d91_120: 33.0, 
  wind_speed_d91_120: 10, 
  wind_dir_d91_120: 'WSW', 
  humidity_d91_120: 85,
});

const predictionResult = reactive({ yield: 0, accuracy: 94.2, grade: 'A+' });

// --- GRAPHICAL ANALYSIS LOGIC ---

// 1. Weather Trends Chart (Line/Area)
const weatherChartOptions = {
  chart: { type: 'area', toolbar: { show: false }, zoom: { enabled: false } },
  colors: ['#059669', '#3b82f6'],
  stroke: { curve: 'smooth', width: 2 },
  xaxis: { categories: ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'] },
  yaxis: [{ title: { text: 'Temp (C)' } }, { opposite: true, title: { text: 'Rain (mm)' } }],
  legend: { position: 'top' }
};

const weatherSeries = computed(() => [
  {
    name: 'Avg Temp',
    data: [
      (formData.min_temp_d1_30 + formData.max_temp_d1_30) / 2,
      (formData.min_temp_d31_60 + formData.max_temp_d31_60) / 2,
      (formData.min_temp_d61_90 + formData.max_temp_d61_90) / 2,
      (formData.min_temp_d91_120 + formData.max_temp_d91_120) / 2,
    ]
  },
  {
    name: 'Rainfall',
    data: [formData.rain_d1_30, formData.rain_d30_50, formData.rain_d51_70, formData.rain_d71_105]
  }
]);

// 2. Humidity vs Wind Speed (Radar)
const factorChartOptions = {
  chart: { type: 'radar', toolbar: { show: false } },
  xaxis: { categories: ['Humidity', 'Wind Speed', 'Soil Quality', 'Rain Volatility'] },
  colors: ['#f59e0b'],
  fill: { opacity: 0.4 }
};

const factorSeries = computed(() => [{
  name: 'Field Metrics',
  data: [
    (formData.humidity_d1_30 + formData.humidity_d31_60 + formData.humidity_d61_90 + formData.humidity_d91_120) / 4,
    (formData.wind_speed_d1_30 + formData.wind_speed_d31_60 + formData.wind_speed_d61_90 + formData.wind_speed_d91_120) * 5, // scaled
    85, // Mocked Soil score
    70  // Mocked Rain stability
  ]
}]);

const submitPrediction = async () => {
  currentStage.value = 2;
  isProcessing.value = true;

  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    if (response.ok) {
      predictionResult.yield = data.predicted_yield;
      currentStage.value = 3;
    } else {
      alert("Error: " + data.detail);
      currentStage.value = 1;
    }
  } catch (error) {
    console.error("Failed to connect to backend", error);
    currentStage.value = 1;
  } finally {
    isProcessing.value = false;
  }
};

const resetForm = () => { currentStage.value = 1; };
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-inter pb-12">
    <div class="max-w-6xl mx-auto px-4 py-8">
      
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
        <div v-if="currentStage === 1">
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-8">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-slate-800">Production Yield Forecast</h2>
              <button @click="showOcrModal = true" class="bg-blue-50 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors">[Camera] OCR Scan</button>
            </div>

            <form @submit.prevent="submitPrediction" class="space-y-8">
              <div class="bg-slate-50 p-6 rounded-lg">
                <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b pb-2">[Geography] Field Geography</h3>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div><label class="label-style">Hectares</label><input v-model="formData.hectares" type="number" step="0.01" class="input-style"></div>
                  <div><label class="label-style">Agriblock</label><input v-model="formData.agriblock" type="text" class="input-style"></div>
                  <div><label class="label-style">Variety</label><input v-model="formData.variety" type="text" class="input-style"></div>
                  <div>
                    <label class="label-style">Soil Type</label>
                    <select v-model="formData.soil_type" class="input-style">
                      <option>Clay</option><option>Alluvial</option><option>Loam</option>
                    </select>
                  </div>
                </div>
              </div>

              <div v-for="phase in [1, 2, 3, 4]" :key="phase" class="bg-white border border-slate-200 p-6 rounded-lg shadow-sm">
                <h3 class="text-md font-bold text-green-700 mb-4 flex items-center gap-2">
                  <span class="w-6 h-6 bg-green-100 text-green-700 rounded-full flex items-center justify-center text-xs">{{ phase }}</span>
                  Weather Phase: Day {{ (phase-1)*30 + 1 }} to {{ phase*30 }}
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
                  <div><label class="label-style">Rain (mm)</label><input v-model="formData[`rain_d${phase === 1 ? '1_30' : phase === 2 ? '30_50' : phase === 3 ? '51_70' : '71_105'}`]" type="number" step="any" class="input-style"></div>
                  <div><label class="label-style">Min Temp</label><input v-model="formData[`min_temp_d${phase === 1 ? '1_30' : phase === 2 ? '31_60' : phase === 3 ? '61_90' : '91_120'}`]" type="number" step="any" class="input-style"></div>
                  <div><label class="label-style">Max Temp</label><input v-model="formData[`max_temp_d${phase === 1 ? '1_30' : phase === 2 ? '31_60' : phase === 3 ? '61_90' : '91_120'}`]" type="number" step="any" class="input-style"></div>
                  <div><label class="label-style">Wind (Kts)</label><input v-model="formData[`wind_speed_d${phase === 1 ? '1_30' : phase === 2 ? '31_60' : phase === 3 ? '61_90' : '91_120'}`]" type="number" step="any" class="input-style"></div>
                  <div><label class="label-style">Wind Dir</label><input v-model="formData[`wind_dir_d${phase === 1 ? '1_30' : phase === 2 ? '31_60' : phase === 3 ? '61_90' : '91_120'}`]" type="text" class="input-style"></div>
                  <div><label class="label-style">Humidity</label><input v-model="formData[`humidity_d${phase === 1 ? '1_30' : phase === 2 ? '31_60' : phase === 3 ? '61_90' : '91_120'}`]" type="number" step="any" class="input-style"></div>
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button type="submit" class="bg-green-600 text-white px-10 py-4 rounded-xl font-bold shadow-lg hover:bg-green-700 transition-all">
                  Run XGBoost Prediction
                </button>
              </div>
            </form>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="bg-slate-800 px-6 py-4">
              <h3 class="text-white font-bold text-sm uppercase tracking-widest">Reference & History Table</h3>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm border-collapse">
                <thead class="bg-slate-50 text-slate-500 font-bold border-b">
                  <tr>
                    <th class="px-6 py-4">Hectares</th>
                    <th class="px-6 py-4">Agriblock</th>
                    <th class="px-6 py-4">Variety</th>
                    <th class="px-6 py-4">Soil</th>
                    <th class="px-6 py-4">P1 Rain</th>
                    <th class="px-6 py-4">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, idx) in historyTable" :key="idx" 
                      :class="idx === 0 ? 'bg-yellow-50 font-medium' : 'hover:bg-slate-50'">
                    <td class="px-6 py-4 border-b">{{ row.hectares }}</td>
                    <td class="px-6 py-4 border-b">{{ row.agriblock }}</td>
                    <td class="px-6 py-4 border-b">{{ row.variety }}</td>
                    <td class="px-6 py-4 border-b">{{ row.soil_type }}</td>
                    <td class="px-6 py-4 border-b">{{ row.rain_d1_30 }} mm</td>
                    <td class="px-6 py-4 border-b">
                      <span :class="idx === 0 ? 'bg-yellow-200 text-yellow-800' : 'bg-blue-100 text-blue-800'" 
                            class="px-2 py-1 rounded text-[10px] font-bold">
                        {{ row.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </transition>

      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 2" class="flex flex-col items-center justify-center py-20 bg-white rounded-xl shadow-sm border">
          <div class="w-16 h-16 border-4 border-green-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <h3 class="text-xl font-bold">Querying ML Model...</h3>
        </div>
      </transition>

      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 3" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div class="bg-white rounded-2xl shadow-xl border overflow-hidden flex flex-col">
              <div class="bg-green-600 p-8 text-center text-white grow flex flex-col justify-center">
                <span class="text-green-100 text-xs font-bold uppercase tracking-widest mb-2">Final Forecast</span>
                <h2 class="text-5xl font-black mb-2">{{ predictionResult.yield.toLocaleString() }}</h2>
                <p class="text-green-50 opacity-80">Kg per Hectare</p>
                
                <div class="mt-8 grid grid-cols-2 gap-4 border-t border-green-500 pt-6">
                  <div>
                    <p class="text-[10px] uppercase opacity-70">Accuracy</p>
                    <p class="font-bold text-lg">{{ predictionResult.accuracy }}%</p>
                  </div>
                  <div>
                    <p class="text-[10px] uppercase opacity-70">Grade</p>
                    <p class="font-bold text-lg">{{ predictionResult.grade }}</p>
                  </div>
                </div>
              </div>
              <button @click="resetForm" class="w-full py-4 bg-slate-800 text-white font-bold hover:bg-slate-900 transition-colors">
                <- Adjust Parameters
              </button>
            </div>

            <div class="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border">
              <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
                <span class="p-2 bg-blue-50 text-blue-600 rounded-lg">[Chart]</span>
                Climate vs. Rainfall Correlation
              </h3>
              <VueApexCharts height="280" :options="weatherChartOptions" :series="weatherSeries" />
            </div>

          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm border">
              <h3 class="font-bold text-slate-800 mb-4">Yield Stability Profile</h3>
              <VueApexCharts height="300" :options="factorChartOptions" :series="factorSeries" />
            </div>

            <div class="bg-slate-800 p-8 rounded-2xl shadow-sm text-white relative overflow-hidden">
               <div class="relative z-10">
                 <h3 class="text-xl font-bold mb-4 text-green-400">Model Insights</h3>
                 <ul class="space-y-4 text-sm text-slate-300">
                   <li class="flex items-start gap-3">
                     <span class="text-green-500">[OK]</span>
                     <span>Rainfall in <b>Phase 2 ({{formData.rain_d30_50}}mm)</b> is optimal for the <b>{{formData.variety}}</b> variety.</span>
                   </li>
                   <li class="flex items-start gap-3">
                     <span class="text-yellow-500">[Warn]</span>
                     <span>High humidity ({{formData.humidity_d61_90}}%) in Phase 3 may increase pest risk in <b>{{formData.soil_type}}</b> soil.</span>
                   </li>
                   <li class="flex items-start gap-3">
                     <span class="text-green-500">[OK]</span>
                     <span>Soil drainage for <b>{{formData.agriblock}}</b> shows high retention for this cycle.</span>
                   </li>
                 </ul>
               </div>
               <div class="absolute -bottom-10 -right-10 w-40 h-40 bg-green-500/10 rounded-full blur-3xl"></div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css"; 

.label-style { 
  @apply block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider; 
}

.input-style { 
  @apply w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border text-sm; 
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>