#!/usr/bin/env python3
"""
LlamaParse Converter Script
A utility script that uses LlamaParse to convert files to structured data.
Supports local files and S3 storage.
"""
import argparse
import os
import sys
import json
import logging
import tempfile
import traceback
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Dict, Any, List, Union
from pathlib import Path
from dotenv import load_dotenv
from llama_parse import LlamaParse

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
def setup_logging():
    """Configure simple logging"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create logs directory
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Use current date for log filename
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'{current_date}.log')
    
    # Configure root logger with file handler only
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    file_handler.setLevel(logging.ERROR)
    
    # Configure the root logger
    logging.basicConfig(level=logging.ERROR, format=log_format, 
                      datefmt=date_format, handlers=[file_handler])
    return logging.getLogger()

def get_output_path(input_path: str, output_format: str) -> str:
    """Generate an output path by replacing the input file extension"""
    # Get the path without extension
    root, _ = os.path.splitext(input_path)
    
    # Add the extension based on output format
    if output_format == "markdown":
        return f"{root}.md"
    elif output_format == "text":
        return f"{root}.txt"
    else:
        return f"{root}.{output_format}"

def download_from_s3(file_path: str) -> str:
    """Download a file from S3 to a local temporary file"""
    try:
        bucket = os.environ.get("S3_BUCKET_NAME")
        if not bucket:
            logging.error("S3_BUCKET_NAME environment variable is not set")
            raise ValueError("S3_BUCKET_NAME environment variable is not set")
        
        # Remove any leading slashes
        key = file_path.lstrip('/')
        
        s3_client = boto3.client('s3')
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            s3_client.download_file(bucket, key, temp_file.name)
            return temp_file.name
        except ClientError as e:
            logging.error(f"Error downloading file from S3: {e}")
            os.unlink(temp_file.name)
            sys.exit(1)
    except ImportError:
        logging.error("boto3 module not found. Please install it to use S3 functionality.")
        sys.exit(1)

def upload_to_s3(local_path: str, s3_path: str) -> None:
    """Upload a file to S3"""
    try:
        bucket = os.environ.get("S3_BUCKET_NAME")
        if not bucket:
            logging.error("S3_BUCKET_NAME environment variable is not set")
            raise ValueError("S3_BUCKET_NAME environment variable is not set")
        
        # Remove any leading slashes
        key = s3_path.lstrip('/')
        
        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(local_path, bucket, key)
        except ClientError as e:
            logging.error(f"Error uploading file to S3: {e}")
            sys.exit(1)
    except ImportError:
        logging.error("boto3 module not found. Please install it to use S3 functionality.")
        sys.exit(1)

def convert_document(file_path: str, output_format: str = "json") -> Dict[str, Any]:
    """Convert the given file using LlamaParse"""
    api_key = os.environ.get("LLAMAPARSE_API_KEY")
    if not api_key:
        logging.error("LLAMAPARSE_API_KEY environment variable is not set")
        raise ValueError("LLAMAPARSE_API_KEY environment variable is not set")
    
    # Check for a non-empty S3 bucket name
    bucket_name = os.environ.get("S3_BUCKET_NAME", "")
    use_s3 = bucket_name and len(bucket_name.strip()) > 0
    local_temp_file = None
    
    try:
        # Handle file retrieval based on whether S3 is enabled using ternary-like structure
        if use_s3:
            local_temp_file = download_from_s3(file_path)
            actual_file_path = local_temp_file
        else:
            # Regular local file - validate existence first
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")
            actual_file_path = file_path
        
        # Generate output path based on input path
        output_file = get_output_path(file_path, output_format)
        
        # Initialize the LlamaParse client
        parser = LlamaParse(api_key=api_key, verbose=False)
        
        # Process the file with LlamaParse
        try:
            # Use the LlamaParse library to get result in requested format(s)
            if output_format == "all":
                # Process in all formats when "all" is specified
                formats = ["json", "markdown", "text"]
                results = {}
                
                for fmt in formats:
                    # Generate output path for this format
                    format_output_file = get_output_path(file_path, fmt)
                    
                    try:
                        if fmt == "json":
                            # Get JSON result using the official API
                            result = parser.get_json_result(actual_file_path)
                        elif fmt == "markdown":
                            # For markdown, parse and extract just the markdown content
                            parse_result = parser.parse(actual_file_path)
                            # Extract the actual markdown content from each page
                            markdown_content = ""
                            try:
                                # Combine markdown content from all pages
                                for page in parse_result.pages:
                                    markdown_content += page.md + "\n\n"
                                result = markdown_content.strip()
                            except (AttributeError, TypeError):
                                # Fallback if structure isn't as expected
                                result = str(parse_result)
                        else:  # text
                            # For text, parse and extract just the text content
                            parse_result = parser.parse(actual_file_path)
                            # Extract the actual text content from each page
                            text_content = ""
                            try:
                                # Combine text content from all pages
                                for page in parse_result.pages:
                                    text_content += page.text + "\n\n"
                                result = text_content.strip()
                            except (AttributeError, TypeError):
                                # Fallback if structure isn't as expected
                                result = str(parse_result)
                        
                        # Save result for this format
                        results[fmt] = result
                        
                        # Handle output based on whether S3 is enabled
                        if use_s3:
                            # For S3: Create a temporary file and upload it
                            with tempfile.NamedTemporaryFile(delete=False) as temp_out:
                                if fmt == "json":
                                    json.dump(result, temp_out, indent=2)
                                else:
                                    temp_out.write(result.encode('utf-8'))
                                temp_out_path = temp_out.name
                            
                            # Upload the temporary file to S3
                            upload_to_s3(temp_out_path, format_output_file)
                            
                            # Clean up temporary output file
                            os.unlink(temp_out_path)
                        else:
                            # For local: Write directly to the output file
                            if fmt == "json":
                                with open(format_output_file, "w") as f:
                                    json.dump(result, f, indent=2)
                            else:
                                with open(format_output_file, "w") as f:
                                    f.write(result)
                        
                        print(f"Created {fmt} output: {format_output_file}")
                    except AttributeError as ae:
                        logging.warning(f"Format '{fmt}' not supported by current LlamaParse version: {ae}")
                        print(f"Warning: Format '{fmt}' not supported by current LlamaParse version")
                        if fmt == "json":
                            raise  # JSON format is essential
                
                # Return all results
                return results
            else:
                # Process in a single format
                try:
                    if output_format == "json":
                        result = parser.get_json_result(actual_file_path)
                    elif output_format == "markdown":
                        # For markdown, parse and extract just the markdown content
                        parse_result = parser.parse(actual_file_path)
                        # Extract the actual markdown content from each page
                        markdown_content = ""
                        try:
                            # Combine markdown content from all pages
                            for page in parse_result.pages:
                                markdown_content += page.md + "\n\n"
                            result = markdown_content.strip()
                        except (AttributeError, TypeError):
                            # Fallback if structure isn't as expected
                            result = str(parse_result)
                    else:  # text
                        # For text, parse and extract just the text content
                        parse_result = parser.parse(actual_file_path)
                        # Extract the actual text content from each page
                        text_content = ""
                        try:
                            # Combine text content from all pages
                            for page in parse_result.pages:
                                text_content += page.text + "\n\n"
                            result = text_content.strip()
                        except (AttributeError, TypeError):
                            # Fallback if structure isn't as expected
                            result = str(parse_result)
                    
                    # Handle output based on whether S3 is enabled
                    if use_s3:
                        # For S3: Create a temporary file and upload it
                        with tempfile.NamedTemporaryFile(delete=False) as temp_out:
                            if output_format == "json":
                                json.dump(result, temp_out, indent=2)
                            else:
                                temp_out.write(result.encode('utf-8'))
                            temp_out_path = temp_out.name
                        
                        # Upload the temporary file to S3
                        upload_to_s3(temp_out_path, output_file)
                        
                        # Clean up temporary output file
                        os.unlink(temp_out_path)
                    else:
                        # For local: Write directly to the output file
                        if output_format == "json":
                            with open(output_file, "w") as f:
                                json.dump(result, f, indent=2)
                        else:
                            with open(output_file, "w") as f:
                                f.write(result)
                    
                    print(f"Created {output_format} output: {output_file}")
                    return result
                except AttributeError as ae:
                    logging.error(f"Format '{output_format}' not supported by current LlamaParse version: {ae}")
                    raise ValueError(f"Format '{output_format}' not supported by current LlamaParse version")
            
        except Exception as e:
            logging.error(f"Error parsing document with LlamaParse: {e}")
            raise
            
    except Exception as e:
        logging.error(f"Unexpected error during document conversion: {str(e)}")
        # Clean up temp file if we created one - safer approach
        if local_temp_file and os.path.exists(local_temp_file):
            os.unlink(local_temp_file)
        raise

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Convert documents using LlamaParse. Supports local files and S3 storage.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument("file", help="Path to the file to convert. Uses S3 if S3_BUCKET_NAME is set, otherwise local file system.")
    
    # Optional arguments
    parser.add_argument("-f", "--format", choices=["json", "markdown", "text", "all"], 
                      default="all", help="Output format. Use 'all' or omit to generate all formats.")
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging()
    
    try:
        # Single print statement to indicate processing has begun
        print(f"Processing: {args.file}")
        
        result = convert_document(file_path=args.file, output_format=args.format)
        
        # Summary message after successful processing
        if args.format == "all":
            print(f"Successfully processed {args.file} in all formats.")
        else:
            print(f"Successfully processed {args.file} in {args.format} format.")
            
    except Exception as e:
        logging.error(f"Error during execution: {e}")
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()