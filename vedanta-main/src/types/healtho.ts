export interface ChatRequest {
  message: string;
  symptoms: Array<{
    symptom: string;
    hasSymptom: boolean;
  }>;
}

export interface ChatResponse {
  response: string;
  is_question: boolean;
  symptom?: string;
  options?: string[];
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  model_loaded: boolean;
}
