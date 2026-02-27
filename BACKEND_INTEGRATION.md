# Backend Integration Guide

This frontend is now ready to integrate with your backend API and ML model. Follow these steps to connect real data and analysis.

## API Integration Points

### 1. Content Analysis Endpoint

**Location**: `src/components/Dashboard.jsx` - `handleAnalyze()` function (Line ~50)

**Current Implementation**: Sample data simulation
**Next Step**: Replace with actual API call

```javascript
// TODO: Replace this code block:
// const response = await fetch('http://localhost:5000/api/analyze', {
//   method: 'POST',
//   body: formData
// })
// const data = await response.json()

// Expected Request Format:
// POST /api/analyze
// Content-Type: multipart/form-data
// Body:
// - text: string (required) - Social media content to analyze
// - image: file (optional) - Image file for multimodal analysis
// - followers: boolean (optional) - Include follower count
// - accountAge: boolean (optional) - Include account age
// - engagementRate: boolean (optional) - Include engagement rate

// Expected Response Format:
{
  "riskScore": 82,              // 0-100 deception risk
  "verdict": "DECEPTIVE",       // Classification: DECEPTIVE, SUSPICIOUS, AUTHENTIC
  "textScore": 88,              // Text analysis risk 0-100
  "imageScore": 42,             // Image analysis risk 0-100
  "trustScore": 12,             // Account trust 0-100
  "reasons": [
    {
      "title": "Reason Title",
      "description": "Detailed explanation of why flagged"
    }
  ]
}
```

### 2. Recent Analysis History Endpoint

**Location**: `src/components/Dashboard.jsx` - `recentAnalysis` variable (Line ~104)

**Current Implementation**: Static sample data
**Next Step**: Fetch from database

```javascript
// TODO: Add useEffect hook to fetch analysis history
// GET /api/analysis-history
// Response: Array of analysis records with date, content, risk, status
```

## Environment Variables

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
```

## Backend Requirements

### Model Outputs
Your ML model should provide:
- **Risk Score**: 0-100 numerical value
- **Text Component Score**: 0-100 for text-based deception markers
- **Image Component Score**: 0-100 for image manipulation detection
- **Trust Score**: 0-100 for account credibility
- **Explainable Reasons**: List of contributing factors

### API Endpoints Required
1. `POST /api/analyze` - Analyze content
2. `GET /api/analysis-history` - Fetch user's analysis history
3. `GET /api/analysis/:id` - Get detailed results
4. `POST /api/export-report` - Export analysis as PDF/report

## State Management

Current state variables:
```javascript
const [textContent, setTextContent] = useState('')        // User input
const [selectedImage, setSelectedImage] = useState(null)  // Selected image file
const [metadata, setMetadata] = useState({...})           // User metadata selections
const [loading, setLoading] = useState(false)             // API loading state
const [error, setError] = useState(null)                  // Error messages
const [riskScore, setRiskScore] = useState(null)          // Risk score from API
const [analysisResult, setAnalysisResult] = useState(null)// Full analysis result
```

## Error Handling

The frontend currently handles:
- Validation: Empty content input
- Network errors: Try-catch with user-friendly messages
- Loading state: "Analyzing..." button state
- Error display: Red error box above analyze button

Add backend error handling for:
- Invalid file formats
- File size limits
- API timeout
- Server errors (500)

## Performance Optimization

Once backend is live:
1. Add request cancellation for rapid consecutive requests
2. Implement request debouncing
3. Cache analysis results locally
4. Add pagination for history table
5. Implement lazy loading for images

## Testing

### Sample Test Data
```javascript
const testContent = "Breaking news: New policy changes government structure!!!"
// Expected: HIGH RISK, >70 score

const mockResponse = {
  riskScore: 82,
  verdict: "DECEPTIVE",
  textScore: 88,
  imageScore: 42,
  trustScore: 12,
  reasons: [...]
}
```

### API Testing Tools
- Postman: For endpoint testing
- Thunder Client: VS Code extension
- curl: Command line testing

## Next Steps

1. ✅ Frontend UI complete
2. ⏳ Implement `/api/analyze` endpoint
3. ⏳ Integrate ML model
4. ⏳ Set up result storage
5. ⏳ Test end-to-end flow
6. ⏳ Deploy to production

## Support

For integration issues:
- Check browser console for errors
- Verify API endpoint URLs
- Test API responses with Postman first
- Add console.log() in handleAnalyze() for debugging

---

**Frontend Status**: ✅ Ready for Backend Integration
**Last Updated**: February 27, 2026
