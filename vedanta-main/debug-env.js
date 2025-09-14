// Debug script to check environment variables
console.log('=== ENVIRONMENT DEBUG ===');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('All environment variables:');
Object.keys(process.env).forEach(key => {
  if (key.includes('GEMINI') || key.includes('VITE')) {
    console.log(`${key}: ${process.env[key]}`);
  }
});
console.log('=== END DEBUG ===');