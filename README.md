# FINd — Find Images Now

FINd is an open-source perceptual image hashing library that generates 256-bit hash fingerprints from images, enabling efficient similarity detection and duplicate clustering at scale.

## Installation

### 1. Clone the Repository

```bash
git clone https://anonymous.4open.science/r/find-images-now-3FD2
cd find-images-now-3FD2
```

### 2. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

The .env file contains the following default values; these can be adjusted if your environment requires different settings:
| Variable | Default | Description |
|----------|---------|-------------|
| `APP_HOST` | `0.0.0.0` | Host address for the API server |
| `APP_PORT` | `8945` | Port for the API server (required by FIN) |
| `LOG_LEVEL` | `DEBUG` | Logging level: DEBUG, INFO, WARNING, ERROR |
| `APP_ENV` | `development` | Runtime environment of the application |

 ### 3. Install Dependencies

```bash
# Standard installation:
pip install .

# Or, for development and testing:
pip install -e ".[dev]"
```
---

## How to Run

### Option 1: Local Development

```bash
python run.py
```

### Option 2: Docker Compose (Recommended)

```bash
docker-compose up --build
```

### Option 3: Docker

```bash
docker build -t find-images-now .
docker run -p 8945:8945 --env-file .env find-images-now

```

---

## API Documentation


### Endpoint: `/compare`

Compares two images and returns their FINd hashes and Hamming distance.

**Method:** `POST`  
**Port:** `8945`  
**URL:** `http://127.0.0.1:8945/compare`

**Input:**
- `image1` — first image file
- `image2` — second image file

**Output:**

```json
{
  "image1_hash": "393b266d65a694dc...",
  "image2_hash": "18bb6c674cae94cc...",
  "distance": 44
}
```

**Example:**

```bash
curl -X POST "http://127.0.0.1:8945/compare" \
-F "image1=@image1.jpg" \
-F "image2=@image2.jpg"
```

**Distance Interpretation:**
- `0` — identical images
- Smaller distance — greater visual similarity
- Larger distance — greater visual dissimilarity

> **Note:** The API is self-documenting via OpenAPI. Once the server is running, you can access the interactive Swagger UI at `http://127.0.0.1:8945/docs`

---

## How to Run Tests

Ensure you have installed the development dependencies:
```bash
pip install -e ".[dev]"
```

Then run the test suite:
```bash
pytest tests/ -v
```

**Expected output:**

```
tests/test_FINd.py::TestFINdOptimisation::test_hash_consistency PASSED                                                             
tests/test_FINd.py::TestFINdOptimisation::test_hash_length PASSED                                                                  
tests/test_FINd.py::TestFINdOptimisation::test_hash_not_none PASSED                                                                
tests/test_FINd.py::TestFINdOptimisation::test_optimisation_drift_threshold PASSED                                                 
tests/test_FINd.py::TestFINdOptimisation::test_rectangle_image_raises_error PASSED                                                 
tests/test_api.py::TestCompareEndpoint::test_invalid_file_type PASSED                                                              
tests/test_api.py::TestCompareEndpoint::test_known_distance PASSED                                                                 
tests/test_api.py::TestCompareEndpoint::test_missing_image PASSED                                                                  
tests/test_api.py::TestCompareEndpoint::test_non_square_image PASSED                                                               
tests/test_api.py::TestCompareEndpoint::test_same_image PASSED                                                                     
tests/test_api.py::TestCompareEndpoint::test_valid_request PASSED 
11 passed
```
---

## Limitations

- The optimised FINd implementation only supports square images. Non-square images will return a `400` error with a descriptive message.
- The optimised implementation may produce hashes with a drift of up to 32 bits from the original FINd due to differences in boundary handling.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.