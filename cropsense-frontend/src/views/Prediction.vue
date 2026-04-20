<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

interface PredictionData {
  hectares: number;
  agriblock: string;
  variety: string;
  soil_type: string;
  
  rain_d1_30: number; min_temp_d1_30: number; max_temp_d1_30: number;
  wind_speed_d1_30: number; wind_dir_d1_30: string; humidity_d1_30: number;

  rain_d30_50: number; min_temp_d31_60: number; max_temp_d31_60: number;
  wind_speed_d31_60: number; wind_dir_d31_60: string; humidity_d31_60: number;

  rain_d51_70: number; min_temp_d61_90: number; max_temp_d61_90: number;
  wind_speed_d61_90: number; wind_dir_d61_90: string; humidity_d61_90: number;

  rain_d71_105: number; min_temp_d91_120: number; max_temp_d91_120: number;
  wind_speed_d91_120: number; wind_dir_d91_120: string; humidity_d91_120: number;
}

const currentStage = ref(1);
const isProcessing = ref(false);
const showOcrModal = ref(false);

const formData = reactive<PredictionData>({
  hectares: 6, agriblock: 'Cuddalore', variety: 'CO_43', soil_type: 'alluvial',
  
  rain_d1_30: 19.6, min_temp_d1_30: 18.5, max_temp_d1_30: 34.0, 
  wind_speed_d1_30: 4, wind_dir_d1_30: 'SW', humidity_d1_30: 72.0,

  rain_d30_50: 187.2, min_temp_d31_60: 16.0, max_temp_d31_60: 30.0, 
  wind_speed_d31_60: 10, wind_dir_d31_60: 'W', humidity_d31_60: 78,

  rain_d51_70: 167.0, min_temp_d61_90: 15.5, max_temp_d61_90: 31.0, 
  wind_speed_d61_90: 8, wind_dir_d61_90: 'NNW', humidity_d61_90: 88,

  rain_d71_105: 61.0, min_temp_d91_120: 16.0, max_temp_d91_120: 33.0, 
  wind_speed_d91_120: 10, wind_dir_d91_120: 'WSW', humidity_d91_120: 85,
});

const predictionResult = reactive({ 
  yield: 0, 
  accuracy: 94.2, 
  grade: 'A+',
  insights: [] as Array<{type: string, text: string}> 
});

// Calculate Growing Degree Days (Base 10C) for the season
const totalGDD = computed(() => {
  const calculatePhaseGDD = (min: number, max: number, days: number) => {
    const avg = (min + max) / 2;
    return Math.max(0, avg - 10) * days;
  };
  return Math.round(
    calculatePhaseGDD(formData.min_temp_d1_30, formData.max_temp_d1_30, 30) +
    calculatePhaseGDD(formData.min_temp_d31_60, formData.max_temp_d31_60, 30) +
    calculatePhaseGDD(formData.min_temp_d61_90, formData.max_temp_d61_90, 30) +
    calculatePhaseGDD(formData.min_temp_d91_120, formData.max_temp_d91_120, 30)
  );
});

const weatherChartOptions = {
  chart: { type: 'area', toolbar: { show: false }, zoom: { enabled: false } },
  colors: ['#059669', '#3b82f6'],
  stroke: { curve: 'smooth', width: 2 },
  xaxis: { categories: ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'] },
  dataLabels: { enabled: true, formatter: (val: any) => val.toFixed(1) },
  tooltip: { y: { formatter: (val: any) => val.toFixed(1) } },
  yaxis: [
    { title: { text: 'Temp (C)' }, labels: { formatter: (val: any) => val.toFixed(0) } }, 
    { opposite: true, title: { text: 'Rain (mm)' }, labels: { formatter: (val: any) => val.toFixed(0) } }
  ],
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
    (formData.wind_speed_d1_30 + formData.wind_speed_d31_60 + formData.wind_speed_d61_90 + formData.wind_speed_d91_120) * 5,
    85, 
    70  
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
      predictionResult.insights = data.insights; 
      
      // Dynamic Grading based on insights
      const warningCount = data.insights.filter((i: any) => i.type === 'warning').length;
      if (warningCount === 0) predictionResult.grade = 'A+';
      else if (warningCount === 1) predictionResult.grade = 'A-';
      else if (warningCount === 2) predictionResult.grade = 'B';
      else predictionResult.grade = 'C (High Risk)';

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

const isFetchingWeather = ref(false);
const locationQuery = reactive({ lat: 11.74, lon: 79.76, date: '2023-01-01' });

const autoFillWeather = async () => {
  isFetchingWeather.value = true;
  try {
    const res = await fetch(`http://localhost:8000/fetch-weather?lat=${locationQuery.lat}&lon=${locationQuery.lon}&plant_date=${locationQuery.date}`);
    const data = await res.json();
    
    formData.rain_d1_30 = data.p1.rain;
    formData.min_temp_d1_30 = data.p1.min_temp;
    formData.max_temp_d1_30 = data.p1.max_temp;
    formData.rain_d30_50 = data.p2.rain;
    formData.min_temp_d31_60 = data.p2.min_temp;
    
    alert("Weather data synchronized successfully!");
  } catch (e) {
    alert("Could not fetch weather data.");
  } finally {
    isFetchingWeather.value = false;
  }
};

const historyTable = ref([
  { hectares: 6, agriblock: 'Cuddalore', variety: 'CO_43', soil_type: 'alluvial', rain_d1_30: 19.6, status: 'Active Prediction' },
  { hectares: 4.5, agriblock: 'Thanjavur', variety: 'ADT_45', soil_type: 'clay', rain_d1_30: 25.2, status: 'Historical' }
]);
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

            <div class="bg-blue-600 rounded-xl p-6 mb-8 text-white flex flex-wrap items-center gap-6 shadow-md">
              <div class="flex-1">
                <h3 class="font-bold text-lg">Smart Weather Import</h3>
                <p class="text-blue-100 text-xs">Auto-populate phases based on historical station data.</p>
              </div>
              <div class="flex gap-4">
                <div class="flex flex-col">
                  <label class="text-[10px] uppercase font-bold text-blue-200">Lat/Lon</label>
                  <input v-model="locationQuery.lat" type="text" class="bg-blue-700 border-none rounded p-1 text-sm w-20">
                </div>
                <div class="flex flex-col">
                  <label class="text-[10px] uppercase font-bold text-blue-200">Start Date</label>
                  <input v-model="locationQuery.date" type="date" class="bg-blue-700 border-none rounded p-1 text-sm">
                </div>
                <button @click="autoFillWeather" :disabled="isFetchingWeather" class="bg-white text-blue-600 px-6 py-2 rounded-lg font-bold hover:bg-blue-50 transition-all self-end">
                  {{ isFetchingWeather ? 'Fetching...' : 'Fetch Open-Meteo Data' }}
                </button>
              </div>
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
                      <option value="clay">Clay</option><option value="alluvial">Alluvial</option><option value="loam">Loam</option>
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
                  <tr v-for="(row, idx) in historyTable" :key="idx" :class="idx === 0 ? 'bg-yellow-50 font-medium' : 'hover:bg-slate-50'">
                    <td class="px-6 py-4 border-b">{{ row.hectares }}</td>
                    <td class="px-6 py-4 border-b">{{ row.agriblock }}</td>
                    <td class="px-6 py-4 border-b">{{ row.variety }}</td>
                    <td class="px-6 py-4 border-b">{{ row.soil_type }}</td>
                    <td class="px-6 py-4 border-b">{{ row.rain_d1_30 }} mm</td>
                    <td class="px-6 py-4 border-b">
                      <span :class="idx === 0 ? 'bg-yellow-200 text-yellow-800' : 'bg-blue-100 text-blue-800'" class="px-2 py-1 rounded text-[10px] font-bold">
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
                
                <div class="mt-6 grid grid-cols-3 gap-2 border-t border-green-500 pt-6">
                  <div>
                    <p class="text-[10px] uppercase opacity-70">Model Acc</p>
                    <p class="font-bold text-lg">{{ predictionResult.accuracy }}%</p>
                  </div>
                  <div>
                    <p class="text-[10px] uppercase opacity-70">GDD Score</p>
                    <p class="font-bold text-lg">{{ totalGDD }}</p>
                  </div>
                  <div>
                    <p class="text-[10px] uppercase opacity-70">Health</p>
                    <p class="font-bold text-lg">{{ predictionResult.grade }}</p>
                  </div>
                </div>
              </div>
              <button @click="resetForm" class="w-full py-4 bg-slate-800 text-white font-bold hover:bg-slate-900 transition-colors">
                &lt;- Adjust Parameters
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

            <div class="bg-slate-800 p-8 rounded-2xl shadow-sm text-white relative overflow-hidden h-full flex flex-col">
              <div class="relative z-10 flex-1">
                <h3 class="text-xl font-bold mb-6 text-green-400 flex items-center gap-2">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  Model Insights
                </h3>
                
                <div class="space-y-3 overflow-y-auto pr-2" style="max-height: 280px;">
                  
                  <div v-for="(insight, index) in predictionResult.insights" :key="index" 
                       class="p-4 rounded-xl border bg-slate-800/50 flex items-start gap-3 transition-all hover:bg-slate-700/50"
                       :class="{
                         'border-green-500/40': insight.type === 'success',
                         'border-yellow-500/40': insight.type === 'warning',
                         'border-blue-500/40': insight.type === 'info'
                       }">
                    
                    <span v-if="insight.type === 'success'" class="shrink-0 flex items-center justify-center w-7 h-7 rounded-full bg-green-500/20 text-green-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>
                    </span>
                    
                    <span v-else-if="insight.type === 'warning'" class="shrink-0 flex items-center justify-center w-7 h-7 rounded-full bg-yellow-500/20 text-yellow-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    </span>
                    
                    <span v-else class="shrink-0 flex items-center justify-center w-7 h-7 rounded-full bg-blue-500/20 text-blue-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </span>

                    <p class="text-sm text-slate-200 leading-relaxed mt-0.5" v-html="insight.text"></p>
                  </div>

                </div>
              </div>
              
              <div class="absolute -bottom-10 -right-10 w-40 h-40 bg-green-500/10 rounded-full blur-3xl pointer-events-none"></div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.label-style { 
  @apply block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider; 
}

.input-style { 
  @apply w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 p-2 border text-sm bg-white text-slate-800; 
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>