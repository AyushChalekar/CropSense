<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Mock data for the "appeasing" visuals
const stats = ref([
  { label: 'Total Forecasts', value: '1,284', icon: '📊', color: 'text-blue-600' },
  { label: 'Avg. Accuracy', value: '94.2%', icon: '🎯', color: 'text-green-600' },
  { label: 'Paddy Varieties', value: '12', icon: '🌾', color: 'text-amber-600' },
  { label: 'Regions Covered', value: '8', icon: '🗺️', color: 'text-purple-600' },
]);

const recentPredictions = ref([
  { id: 1, date: '2023-10-24', crop: 'Rice (Jasmine)', predictedYield: '4.2 Tons/Ha', status: 'High' },
  { id: 2, date: '2023-10-22', crop: 'Rice (Basmati)', predictedYield: '3.8 Tons/Ha', status: 'Optimal' },
  { id: 3, date: '2023-10-20', crop: 'Maize (Hybrid)', predictedYield: '5.1 Tons/Ha', status: 'Excellent' },
]);

const navigateToPredict = () => {
  router.push('/predict');
};
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-12">
    <div class="bg-white border-b border-slate-200 mb-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
                <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">CropSense Dashboard</h1>
                <p class="text-slate-500 font-medium mt-1">Intelligent Paddy Harvest Forecasting System</p>
            </div>
            <button 
                @click="navigateToPredict" 
                class="inline-flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-xl shadow-md transition-all active:scale-95"
            >
                <span>+ New Prediction</span>
            </button>
        </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div v-for="stat in stats" :key="stat.label" class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center gap-4">
            <div class="text-3xl bg-slate-50 w-14 h-14 flex items-center justify-center rounded-xl shadow-inner">
                {{ stat.icon }}
            </div>
            <div>
                <p class="text-sm font-semibold text-slate-500 uppercase tracking-wider">{{ stat.label }}</p>
                <p class="text-2xl font-black text-slate-900">{{ stat.value }}</p>
            </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <section class="lg:col-span-2 bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-xl font-bold text-slate-800">Yield Trend Analysis</h2>
            <select class="bg-slate-50 border border-slate-200 text-sm rounded-lg p-1 text-slate-600 focus:outline-none">
                <option>Last 6 Months</option>
                <option>Last Year</option>
            </select>
          </div>
          
          <div class="relative h-64 w-full bg-slate-50 rounded-xl border border-dashed border-slate-200 flex items-end justify-around px-4 pb-2 group">
            <div class="absolute inset-0 flex flex-col justify-between p-4 pointer-events-none">
                <div class="border-b border-slate-200 w-full h-0"></div>
                <div class="border-b border-slate-200 w-full h-0"></div>
                <div class="border-b border-slate-200 w-full h-0"></div>
            </div>
            <div class="w-12 bg-green-200 hover:bg-green-400 transition-all rounded-t-lg" style="height: 40%"></div>
            <div class="w-12 bg-green-300 hover:bg-green-400 transition-all rounded-t-lg" style="height: 65%"></div>
            <div class="w-12 bg-green-400 hover:bg-green-500 transition-all rounded-t-lg shadow-lg shadow-green-100" style="height: 85%"></div>
            <div class="w-12 bg-green-300 hover:bg-green-400 transition-all rounded-t-lg" style="height: 55%"></div>
            <div class="w-12 bg-green-500 hover:bg-green-600 transition-all rounded-t-lg shadow-lg shadow-green-100" style="height: 95%"></div>
            <div class="w-12 bg-green-400 hover:bg-green-500 transition-all rounded-t-lg" style="height: 75%"></div>
          </div>
          <div class="flex justify-around mt-4 text-xs font-bold text-slate-400 uppercase">
            <span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span>
          </div>
        </section>

        <div class="space-y-8">
            <section class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                <div class="flex items-center gap-2 mb-6">
                    <div class="w-2 h-6 bg-blue-500 rounded-full"></div>
                    <h2 class="text-xl font-bold text-slate-800">System Health</h2>
                </div>
                <div class="space-y-4">
                    <div class="flex justify-between items-center p-3 bg-blue-50/50 rounded-xl border border-blue-100">
                        <span class="text-slate-600 font-semibold">MAE Accuracy</span>
                        <span class="text-blue-700 font-black">0.42</span>
                    </div>
                    <div class="flex justify-between items-center p-3 bg-slate-50 rounded-xl">
                        <span class="text-slate-600 font-semibold">Model</span>
                        <span class="text-slate-800 font-mono text-xs bg-white border border-slate-200 px-2 py-1 rounded">v1.0.2-prod</span>
                    </div>
                    <div class="flex justify-between items-center px-3 py-1">
                        <span class="text-slate-500 text-sm">Server Latency</span>
                        <span class="text-slate-800 text-sm font-bold">24ms</span>
                    </div>
                </div>
            </section>

            <section class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                <h2 class="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                    <span class="text-amber-500">📋</span> Recent Activity
                </h2>
                <div class="space-y-4">
                    <div v-for="prediction in recentPredictions" :key="prediction.id" class="group cursor-pointer">
                        <div class="flex justify-between items-start mb-1">
                            <div>
                                <p class="text-sm font-bold text-slate-800 group-hover:text-green-600 transition-colors">{{ prediction.crop }}</p>
                                <p class="text-[10px] text-slate-400 font-bold uppercase tracking-tighter">{{ prediction.date }}</p>
                            </div>
                            <span class="text-xs font-black px-2 py-1 rounded bg-green-100 text-green-700">{{ prediction.predictedYield }}</span>
                        </div>
                        <div class="w-full bg-slate-100 h-1 rounded-full overflow-hidden">
                            <div class="bg-green-500 h-full w-2/3"></div>
                        </div>
                    </div>
                </div>
            </section>
        </div>

      </div>
    </div>
  </div>
</template>