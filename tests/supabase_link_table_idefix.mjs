import pkg from 'pg'; // PostgreSQL client import

import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Bir üst dizindeki .env dosyasını yükle
dotenv.config({ path: path.resolve(__dirname, '../.env') });


const rawPassword = process.env.PG_PASSWORD;
const encodedPassword = encodeURIComponent(rawPassword);
///const base = process.env.PG_CONNECTION_STRING_BASE;

//const connectionString = base.replace('@', `${encodedPassword}@`);
///const connectionString = `postgresql://postgres.vuoxqclhziyumhrhbsqo:${encodedPassword}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres`;

// Import the Client class from pg package
const { Client } = pkg;

// Initialize PostgreSQL client
const client = new Client({
  connectionString: `postgresql://postgres.vuoxqclhziyumhrhbsqo:${encodedPassword}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres`,
});

// Function to execute a SQL procedure in PostgreSQL
async function executeFunction(functionName) {
  try {
    await client.query(`SELECT ${functionName}();`);
    console.log(`Execution of ${functionName} complete.`);
  } catch (err) {
    console.error(`Error executing ${functionName}:`, err);
  }
}

// Only run the 'create_yeni_scraplar_table' procedure
async function runProcedure() {
  try {
    await client.connect(); // Connect to PostgreSQL
    await executeFunction('create_yeni_scraplar_table');
  } finally {
    await client.end(); // Close the PostgreSQL connection
  }
}

// Run it
runProcedure().catch(err => console.error('Error running procedure:', err));
