from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime, timedelta
import json
from pathlib import Path
import io
import os

app = FastAPI(title="Stream Stats API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to Stream Stats API"}

@app.post("/upload-tsv/")
async def upload_tsv(file: UploadFile = File(...)):
    """Upload a TSV file for analysis"""
    if not file.filename.endswith('.tsv'):
        raise HTTPException(status_code=400, detail="File must be a TSV")
    
    # Save the uploaded file
    file_path = data_dir / f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tsv"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"filename": file_path.name, "status": "File uploaded successfully"}

@app.get("/streaming-stats/")
async def streaming_stats(
    filename: str,
    time_period: str = "monthly",
    store: str = None,
    start_date: str = None,
    end_date: str = None
):
    """Get streaming statistics based on parameters"""
    file_path = data_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Process date parameters
        start_date_dt = datetime.fromisoformat(start_date) if start_date else None
        end_date_dt = datetime.fromisoformat(end_date) if end_date else None
        
        # Calculate last year if dates not provided
        if not start_date_dt and not end_date_dt:
            end_date_dt = datetime.now()
            start_date_dt = end_date_dt - timedelta(days=365)
        
        # Load and process the data
        stats = process_streaming_data(
            file_path, 
            time_period, 
            store, 
            start_date_dt, 
            end_date_dt
        )
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def process_streaming_data(file_path, time_period='monthly', store=None, start_date=None, end_date=None):
    """Process TSV data and return streaming statistics"""
    # Load TSV file
    df = pd.read_csv(file_path, sep='\t')
    
    # Convert date columns to datetime
    df['Reporting Date'] = pd.to_datetime(df['Reporting Date'], errors='coerce')
    df['Sale Month'] = pd.to_datetime(df['Sale Month'], errors='coerce')
    
    # Create a copy to avoid modifying the original
    filtered_df = df.copy()
    
    # Filter by date range if specified
    if start_date:
        filtered_df = filtered_df[filtered_df['Reporting Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Reporting Date'] <= end_date]
    
    # Filter by store if specified
    if store:
        filtered_df = filtered_df[filtered_df['Store'] == store]
    
    # Group by date according to time period
    if time_period == 'daily':
        grouped = filtered_df.groupby(filtered_df['Reporting Date'].dt.date)
    elif time_period == 'weekly':
        grouped = filtered_df.groupby(filtered_df['Reporting Date'].dt.isocalendar().week)
    elif time_period == 'monthly':
        grouped = filtered_df.groupby(filtered_df['Reporting Date'].dt.to_period('M'))
    else:
        raise ValueError("time_period must be 'daily', 'weekly', or 'monthly'")
    
    # Sum quantities for each group
    streams_by_period = grouped['Quantity'].sum().reset_index()
    
    # Convert to dictionary format suitable for JSON serialization
    if time_period == 'daily':
        streams_by_period['Reporting Date'] = streams_by_period['Reporting Date'].astype(str)
        data_dict = streams_by_period.rename(columns={
            'Reporting Date': 'date',
            'Quantity': 'streams'
        }).to_dict('records')
    elif time_period == 'weekly':
        data_dict = streams_by_period.rename(columns={
            'Reporting Date': 'week',
            'Quantity': 'streams'
        }).to_dict('records')
    else:  # monthly
        data_dict = [
            {'month': str(period), 'streams': int(streams)}
            for period, streams in zip(streams_by_period['Reporting Date'], streams_by_period['Quantity'])
        ]
    
    # Calculate total streams
    total_streams = int(filtered_df['Quantity'].sum())
    
    # Get list of available stores for frontend filters
    available_stores = df['Store'].unique().tolist()
    
    return {
        'time_period': time_period,
        'store': store,
        'total_streams': total_streams,
        'data': data_dict,
        'available_stores': available_stores
    }

@app.get("/available-files/")
async def list_available_files():
    """List all available TSV files"""
    files = [f.name for f in data_dir.glob("*.tsv")]
    return {"files": files}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
