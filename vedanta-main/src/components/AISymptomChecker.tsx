import React, { useState } from 'react';
import { Brain, Search, AlertTriangle, CheckCircle, Clock, ArrowRight, TrendingUp, Users, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Symptom {
  id: string;
  name: string;
  severity: 'low' | 'medium' | 'high';
}

interface Assessment {
  condition: string;
  probability: number;
  urgency: 'low' | 'medium' | 'high';
  description: string;
  recommendations: string[];
  specialist: string;
}

const AISymptomChecker = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<Symptom[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [liveStats, setLiveStats] = useState({
    totalChecks: 15847,
    accuracy: 94.7,
    avgTime: 2.3
  });

  // Simulate real-time stats updates
  React.useEffect(() => {
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        totalChecks: prev.totalChecks + Math.floor(Math.random() * 3),
        accuracy: Math.min(99.9, prev.accuracy + (Math.random() - 0.5) * 0.1),
        avgTime: Math.max(1.5, Math.min(3.5, prev.avgTime + (Math.random() - 0.5) * 0.2))
      }));
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const availableSymptoms: Symptom[] = [
    { id: '1', name: 'Headache', severity: 'medium' },
    { id: '2', name: 'Fever', severity: 'medium' },
    { id: '3', name: 'Chest Pain', severity: 'high' },
    { id: '4', name: 'Shortness of Breath', severity: 'high' },
    { id: '5', name: 'Nausea', severity: 'low' },
    { id: '6', name: 'Dizziness', severity: 'medium' },
    { id: '7', name: 'Fatigue', severity: 'low' },
    { id: '8', name: 'Cough', severity: 'low' },
    { id: '9', name: 'Abdominal Pain', severity: 'medium' },
    { id: '10', name: 'Joint Pain', severity: 'low' },
    { id: '11', name: 'Back Pain', severity: 'medium' },
    { id: '12', name: 'Skin Rash', severity: 'low' },
    { id: '13', name: 'Vision Problems', severity: 'medium' },
    { id: '14', name: 'Hearing Loss', severity: 'medium' },
    { id: '15', name: 'Memory Issues', severity: 'medium' }
  ];

  const filteredSymptoms = availableSymptoms.filter(symptom =>
    symptom.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
    !selectedSymptoms.find(s => s.id === symptom.id)
  );

  const addSymptom = (symptom: Symptom) => {
    setSelectedSymptoms([...selectedSymptoms, symptom]);
    setSearchTerm('');
  };

  const removeSymptom = (symptomId: string) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s.id !== symptomId));
  };

  const analyzeSymptoms = async () => {
    if (selectedSymptoms.length === 0) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);
    
    // Simulate progressive AI analysis
    const progressInterval = setInterval(() => {
      setAnalysisProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          const mockAssessment: Assessment = generateMockAssessment(selectedSymptoms);
          setAssessment(mockAssessment);
          setIsAnalyzing(false);
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 200);
  };

  const generateMockAssessment = (symptoms: Symptom[]): Assessment => {
    const hasHighSeverity = symptoms.some(s => s.severity === 'high');
    const hasMediumSeverity = symptoms.some(s => s.severity === 'medium');
    
    if (symptoms.find(s => s.name === 'Chest Pain')) {
      return {
        condition: 'Possible Cardiac Condition',
        probability: 75,
        urgency: 'high',
        description: 'Based on your symptoms, there may be a cardiac-related condition that requires immediate attention.',
        recommendations: [
          'Seek immediate medical attention',
          'Avoid physical exertion',
          'Monitor symptoms closely',
          'Call emergency services if symptoms worsen'
        ],
        specialist: 'Cardiology'
      };
    }
    
    if (symptoms.find(s => s.name === 'Headache') && symptoms.find(s => s.name === 'Fever')) {
      return {
        condition: 'Possible Viral Infection',
        probability: 65,
        urgency: 'medium',
        description: 'Your symptoms suggest a possible viral infection or flu-like illness.',
        recommendations: [
          'Rest and stay hydrated',
          'Monitor temperature regularly',
          'Consider over-the-counter pain relief',
          'Schedule appointment if symptoms persist'
        ],
        specialist: 'General Medicine'
      };
    }
    
    return {
      condition: hasHighSeverity ? 'Requires Medical Attention' : hasMediumSeverity ? 'Monitor Symptoms' : 'Likely Minor Condition',
      probability: hasHighSeverity ? 80 : hasMediumSeverity ? 60 : 40,
      urgency: hasHighSeverity ? 'high' : hasMediumSeverity ? 'medium' : 'low',
      description: 'Based on your reported symptoms, here is our AI assessment of your condition.',
      recommendations: [
        'Monitor symptoms for changes',
        'Stay hydrated and rest',
        'Consider scheduling a consultation',
        'Seek immediate care if symptoms worsen'
      ],
      specialist: 'General Medicine'
    };
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'medium': return 'text-orange-600 bg-orange-50 border-orange-200';
      default: return 'text-green-600 bg-green-50 border-green-200';
    }
  };

  const getUrgencyIcon = (urgency: string) => {
    switch (urgency) {
      case 'high': return <AlertTriangle className="h-5 w-5 text-red-600" />;
      case 'medium': return <Clock className="h-5 w-5 text-orange-600" />;
      default: return <CheckCircle className="h-5 w-5 text-green-600" />;
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg p-6 max-w-4xl mx-auto"
    >
      {/* Header with Live Stats */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <motion.div 
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.5 }}
            className="bg-purple-100 p-3 rounded-full"
          >
            <Brain className="h-6 w-6 text-purple-600" />
          </motion.div>
          <div>
            <h3 className="text-2xl font-bold text-gray-900">AI Symptom Checker</h3>
            <p className="text-gray-600">Describe your symptoms for an AI-powered health assessment</p>
          </div>
        </div>
        
        {/* Live Stats */}
        <div className="flex space-x-4 text-center">
          <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-3 rounded-lg">
            <div className="flex items-center space-x-1 mb-1">
              <Users className="h-4 w-4 text-purple-600" />
              <span className="text-sm font-medium text-purple-600">{liveStats.totalChecks.toLocaleString()}</span>
            </div>
            <p className="text-xs text-gray-600">Total Checks</p>
          </div>
          <div className="bg-gradient-to-br from-emerald-50 to-teal-50 p-3 rounded-lg">
            <div className="flex items-center space-x-1 mb-1">
              <TrendingUp className="h-4 w-4 text-emerald-600" />
              <span className="text-sm font-medium text-emerald-600">{liveStats.accuracy.toFixed(1)}%</span>
            </div>
            <p className="text-xs text-gray-600">Accuracy</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-3 rounded-lg">
            <div className="flex items-center space-x-1 mb-1">
              <Clock className="h-4 w-4 text-blue-600" />
              <span className="text-sm font-medium text-blue-600">{liveStats.avgTime.toFixed(1)}s</span>
            </div>
            <p className="text-xs text-gray-600">Avg Time</p>
          </div>
        </div>
      </div>

      {/* Symptom Search */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search for symptoms..."
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none"
          />
        </div>
        
        {searchTerm && filteredSymptoms.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-40 overflow-y-auto"
          >
            <AnimatePresence>
              {filteredSymptoms.slice(0, 5).map((symptom, index) => (
                <motion.button
                  key={symptom.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ backgroundColor: '#f9fafb' }}
                  onClick={() => addSymptom(symptom)}
                  className="w-full text-left px-4 py-2 hover:bg-gray-50 flex items-center justify-between"
                >
                  <span>{symptom.name}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${getSeverityColor(symptom.severity)}`}>
                    {symptom.severity}
                  </span>
                </motion.button>
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </div>

      {/* Selected Symptoms */}
      {selectedSymptoms.length > 0 && (
        <motion.div 
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mb-6"
        >
          <h4 className="text-lg font-semibold text-gray-900 mb-3">Selected Symptoms</h4>
          <div className="flex flex-wrap gap-2">
            <AnimatePresence>
              {selectedSymptoms.map((symptom, index) => (
                <motion.div
                  key={symptom.id}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  transition={{ delay: index * 0.05 }}
                  className={`px-3 py-2 rounded-full border flex items-center space-x-2 ${getSeverityColor(symptom.severity)}`}
                >
                  <span className="text-sm font-medium">{symptom.name}</span>
                  <motion.button
                    whileHover={{ scale: 1.2 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => removeSymptom(symptom.id)}
                    className="hover:bg-black/10 rounded-full p-1"
                  >
                    ×
                  </motion.button>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      {/* Analyze Button */}
      {selectedSymptoms.length > 0 && !assessment && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={analyzeSymptoms}
            disabled={isAnalyzing}
            className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-8 py-3 rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-50 flex items-center space-x-2"
          >
            {isAnalyzing ? (
              <>
                <motion.div 
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="rounded-full h-5 w-5 border-b-2 border-white"
                />
                <span>Analyzing Symptoms...</span>
              </>
            ) : (
              <>
                <Brain className="h-5 w-5" />
                <span>Analyze with AI</span>
              </>
            )}
          </motion.button>
          
          {isAnalyzing && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">AI Analysis Progress</span>
                <span className="text-sm font-medium text-purple-600">{Math.round(analysisProgress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${analysisProgress}%` }}
                  className="bg-gradient-to-r from-purple-500 to-indigo-500 h-2 rounded-full"
                />
              </div>
              <div className="flex items-center space-x-2 mt-2">
                <Activity className="h-4 w-4 text-purple-500" />
                <span className="text-xs text-gray-500">
                  {analysisProgress < 30 ? 'Processing symptoms...' :
                   analysisProgress < 60 ? 'Analyzing patterns...' :
                   analysisProgress < 90 ? 'Generating assessment...' : 'Finalizing results...'}
                </span>
              </div>
            </motion.div>
          )}
        </motion.div>
      )}

      {/* AI Assessment Results */}
      {assessment && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-200"
        >
          <div className="flex items-center space-x-3 mb-4">
            {getUrgencyIcon(assessment.urgency)}
            <h4 className="text-xl font-bold text-gray-900">AI Assessment Results</h4>
            <div className="ml-auto flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-green-600">Live Analysis</span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h5 className="font-semibold text-gray-900 mb-2">Possible Condition</h5>
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="text-lg text-purple-700 font-medium mb-4"
              >
                {assessment.condition}
              </motion.p>
              
              <h5 className="font-semibold text-gray-900 mb-2">Confidence Level</h5>
              <div className="flex items-center space-x-3 mb-4">
                <div className="flex-1 bg-gray-200 rounded-full h-3">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${assessment.probability}%` }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="bg-gradient-to-r from-purple-500 to-indigo-500 h-3 rounded-full"
                  />
                </div>
                <span className="text-sm font-medium text-gray-700">{assessment.probability}%</span>
              </div>
              
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-gray-600 text-sm"
              >
                {assessment.description}
              </motion.p>
            </div>
            
            <div>
              <h5 className="font-semibold text-gray-900 mb-3">Recommendations</h5>
              <ul className="space-y-2 mb-4">
                <AnimatePresence>
                  {assessment.recommendations.map((rec, index) => (
                    <motion.li 
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 + index * 0.1 }}
                      className="flex items-start space-x-2 text-sm text-gray-600"
                    >
                      <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span>{rec}</span>
                    </motion.li>
                  ))}
                </AnimatePresence>
              </ul>
              
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
                className="bg-white rounded-lg p-4 border border-purple-200"
              >
                <h6 className="font-medium text-gray-900 mb-2">Recommended Specialist</h6>
                <p className="text-purple-600 font-medium">{assessment.specialist}</p>
                <motion.button 
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="mt-3 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm flex items-center space-x-2"
                >
                  <span>Book Appointment</span>
                  <ArrowRight className="h-4 w-4" />
                </motion.button>
              </motion.div>
            </div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
          >
            <p className="text-sm text-yellow-800">
              <strong>Disclaimer:</strong> This AI assessment is for informational purposes only and should not replace professional medical advice. 
              Please consult with a qualified healthcare provider for proper diagnosis and treatment.
            </p>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default AISymptomChecker;