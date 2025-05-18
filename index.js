import express from 'express';
import { spawn } from 'child_process';
import bodyParser from 'body-parser';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static('public'));

// Set EJS as templating engine
app.set('view engine', 'ejs');
app.set('views' ,'backend/views');

// All Polish regions for dropdown (voivodeships and powiats)
const voivodeships = [
  // Voivodeships
  'DOLNOŚLĄSKIE',
  'KUJAWSKO-POMORSKIE',
  'LUBELSKIE',
  'LUBUSKIE',
  'ŁÓDZKIE',
  'MAŁOPOLSKIE',
  'MAZOWIECKIE',
  'OPOLSKIE',
  'PODKARPACKIE',
  'PODLASKIE',
  'POMORSKIE',
  'ŚLĄSKIE',
  'ŚWIĘTOKRZYSKIE',
  'WARMIŃSKO-MAZURSKIE',
  'WIELKOPOLSKIE',
  'ZACHODNIOPOMORSKIE',
  
  // Powiats - DOLNOŚLĄSKIE
  'Powiat bolesławiecki', 'Powiat dzierżoniowski', 'Powiat głogowski', 'Powiat górowski', 'Powiat jaworski',
  'Powiat karkonoski', 'Powiat kamiennogórski', 'Powiat kłodzki', 'Powiat legnicki', 'Powiat lubański',
  'Powiat lubiński', 'Powiat lwówecki', 'Powiat milicki', 'Powiat oleśnicki', 'Powiat oławski',
  'Powiat polkowicki', 'Powiat strzeliński', 'Powiat średzki', 'Powiat świdnicki', 'Powiat trzebnicki',
  'Powiat wałbrzyski', 'Powiat wołowski', 'Powiat wrocławski', 'Powiat ząbkowicki', 'Powiat zgorzelecki',
  'Powiat złotoryjski', 'Powiat m. Jelenia Góra', 'Powiat m. Legnica', 'Powiat m. Wrocław', 'Powiat m. Wałbrzych od 2013',
  
  // Powiats - KUJAWSKO-POMORSKIE
  'Powiat aleksandrowski', 'Powiat brodnicki', 'Powiat bydgoski', 'Powiat chełmiński', 'Powiat golubsko-dobrzyński',
  'Powiat grudziądzki', 'Powiat inowrocławski', 'Powiat lipnowski', 'Powiat mogileński', 'Powiat nakielski', 
  'Powiat radziejowski', 'Powiat rypiński', 'Powiat sępoleński', 'Powiat świecki', 'Powiat toruński', 
  'Powiat tucholski', 'Powiat wąbrzeski', 'Powiat włocławski', 'Powiat żniński', 'Powiat m. Bydgoszcz', 
  'Powiat m. Grudziądz', 'Powiat m. Toruń', 'Powiat m. Włocławek',
  
  // Powiats - LUBELSKIE
  'Powiat bialski', 'Powiat biłgorajski', 'Powiat chełmski', 'Powiat hrubieszowski', 'Powiat janowski',
  'Powiat krasnostawski', 'Powiat kraśnicki', 'Powiat lubartowski', 'Powiat lubelski', 'Powiat łęczyński',
  'Powiat łukowski', 'Powiat opolski', 'Powiat parczewski', 'Powiat puławski', 'Powiat radzyński',
  'Powiat rycki', 'Powiat tomaszowski', 'Powiat włodawski', 'Powiat zamojski', 'Powiat m. Biała Podlaska',
  'Powiat m. Chełm', 'Powiat m. Lublin', 'Powiat m. Zamość',
  
  // Other powiats can be added similarly
  // For brevity, I'm showing only the first few voivodeships' powiats
  // The full list can be included in a similar pattern
];

// Apartment size categories - these must match the training data format
const sizeCategories = [
  { id: 'small', label: 'Small', range: 'do 40 m²' },         // up to 40 square meters
  { id: 'medium', label: 'Medium', range: 'od 40.1 do 60 m²' }, // from 40.1 to 60 m²
  { id: 'large', label: 'Large', range: 'od 60.1 do 80 m²' },  // from 60.1 to 80 m²
  { id: 'xlarge', label: 'Extra Large', range: 'od 80.1 m²' }  // from 80.1 m²
];
// Market types
const marketTypes = [
  { id: 'primary', label: 'Primary Market (New constructions)', value: 'primary market' },
  { id: 'secondary', label: 'Secondary Market (Resale properties)', value: 'secondary market' }
];
// Home route
app.get('/', (req, res) => {
  res.render('index', {
    voivodeships,
    sizeCategories,
    marketTypes,
    formData: {},
    prediction: null,
    error: null
  });
});
// Predict route
app.post('/predict', (req, res) => {
  console.log('Received form data:', req.body);
  
  // Extract form data
  const { voivodeship, sizeCategory, customSize, month, year, marketType } = req.body;
  
  // Validate inputs
  if (!voivodeship || !year || !month || (!sizeCategory && !customSize)) {
    return res.render('index', {
      voivodeships,
      sizeCategories,
      marketTypes,
      formData: req.body,
      prediction: null,
      error: 'Please fill in all required fields'
    });
  }
  // Calculate quarter from month
  const quarter = Math.ceil(parseInt(month) / 3);
  
  // Determine size parameter
  let size = customSize ? `${customSize} m²` : '';
  if (sizeCategory === 'small') size = 'do 40 m²';
  if (sizeCategory === 'medium') size = 'od 40.1 do 60 m²';
  if (sizeCategory === 'large') size = 'od 60.1 do 80 m²';
  if (sizeCategory === 'xlarge') size = 'od 80.1 m²';
  // Default to primary market if not specified
  const market = marketType || 'primary market';
  console.log(`Calling Python with: voivodeship=${voivodeship}, year=${year}, quarter=${quarter}, size=${size}, market=${market}`);
  // Call Python script - use 'python' instead of 'python3' for Windows
  const pythonProcess = spawn('python', [
    'predict.py',
    voivodeship,
    year,
    quarter.toString(),
    size,
    market
  ]);
  let pythonData = '';
  let pythonError = '';
  pythonProcess.stdout.on('data', (data) => {
    pythonData += data.toString();
    console.log(`Python stdout: ${data}`);
  });
  pythonProcess.stderr.on('data', (data) => {
    pythonError += data.toString();
    console.error(`Python stderr: ${data}`);
  });
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    
    if (code !== 0 && !pythonData) {
      return res.render('index', {
        voivodeships,
        sizeCategories,
        marketTypes,
        formData: req.body,
        prediction: null,
        error: `Prediction error: ${pythonError || 'Unknown error occurred'}`
      });
    }
    try {
      // Parse the prediction result and check for fallback message
      const outputLines = pythonData.trim().split('\n');
      const lastLine = outputLines[outputLines.length - 1]; // Get the last line with the prediction
      const predictionResult = parseFloat(lastLine);
      
      if (isNaN(predictionResult)) {
        throw new Error('Invalid prediction result');
      }
      
      // Check if fallback calculation was used
      const usedFallback = pythonError.includes('Primary prediction failed') || 
                           outputLines.some(line => line.includes('Using fallback calculation'));
      
      // Extract economic indicators
      let economicFactors = {
        interestRate: null,
        inflation: null,
        gdp: null,
        unemployment: null,
        apartmentsSold: null
      };
      
      // Look for the economic indicators line
      const economicIndicatorsLine = outputLines.find(line => line.includes('ECONOMIC_INDICATORS'));
      if (economicIndicatorsLine) {
        // Extract each value using regex
        const interestMatch = economicIndicatorsLine.match(/interest=([0-9.]+)/);
        const inflationMatch = economicIndicatorsLine.match(/inflation=([0-9.]+)/);
        const gdpMatch = economicIndicatorsLine.match(/gdp=([0-9.]+)/);
        const unemploymentMatch = economicIndicatorsLine.match(/unemployment=([0-9.]+)/);
        const apartmentsSoldMatch = economicIndicatorsLine.match(/apartments_sold=([0-9]+)/);
        
        economicFactors = {
          interestRate: interestMatch ? interestMatch[1] : null,
          inflation: inflationMatch ? inflationMatch[1] : null,
          gdp: gdpMatch ? gdpMatch[1] : null,
          unemployment: unemploymentMatch ? unemploymentMatch[1] : null,
          apartmentsSold: apartmentsSoldMatch ? apartmentsSoldMatch[1] : null
        };
      }
      
      res.render('index', {
        voivodeships,
        sizeCategories,
        marketTypes,
        formData: req.body,
        prediction: {
          price: predictionResult.toFixed(2),
          voivodeship,
          size,
          market,
          date: `${month}/${year} (Q${quarter})`,
          fallback: usedFallback,
          economicFactors: economicFactors
        },
        error: null
      });
    } catch (error) {
      console.error('Error parsing prediction result:', error);
      res.render('index', {
        voivodeships,
        sizeCategories,
        marketTypes,
        formData: req.body,
        prediction: null,
        error: `Failed to process prediction: ${error.message}`
      });
    }
  });
});
// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
});