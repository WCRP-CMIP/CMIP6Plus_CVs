// prebuild.js
import fs from 'fs';
import path from 'path';

// Define source and destination paths
const static_name = 'data_descriptors'

const CMIP_ROOT = './';
const STATIC_DIR = path.join(process.cwd(), static_name);

// List of directories to copy from CMIP_ROOT to static
const DIRS_TO_COPY = [
  'data_descriptors/',
  // Add other directories as needed
];

function copyDirectory(src, dest) {
  // Create destination directory
  fs.mkdirSync(dest, { recursive: true });
  
  try {
    // Copy the entire directory content
    fs.cpSync(src, dest, { 
      recursive: true,
      force: true,
    });
    console.log(`✓ Copied ${src} to ${dest}`);
  } catch (error) {
    console.error(`× Failed to copy ${src}:`, error);
  }
}

// Clean and recreate static directory
console.log('Preparing static directory...');
if (fs.existsSync(STATIC_DIR)) {
  fs.rmSync(STATIC_DIR, { recursive: true, force: true });
}
fs.mkdirSync(STATIC_DIR, { recursive: true });

// Copy each directory
console.log('\nCopying files...');
for (const dir of DIRS_TO_COPY) {
  const sourcePath = path.join(CMIP_ROOT, dir);
  const destPath = path.join(STATIC_DIR, dir);
  
  // Ensure source exists
  if (!fs.existsSync(sourcePath)) {
    console.error(`× Source does not exist: ${sourcePath}`);
    continue;
  }
  
  // Create parent directories
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  
  // Copy directory
  copyDirectory(sourcePath, destPath);
}

console.log('\nStatic directory preparation complete!');
