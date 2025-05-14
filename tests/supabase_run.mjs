import pkg from 'pg'; // PostgreSQL client import
import { createClient } from '@supabase/supabase-js'; // For Supabase data insertion

import path from 'path';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Bir üst dizindeki .env dosyasını yükle
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const rawPassword = process.env.PG_PASSWORD;
const encodedPassword = encodeURIComponent(rawPassword);
const base = process.env.PG_CONNECTION_STRING_BASE;
// Import the Client class from pg package
const { Client } = pkg;

// Initialize PostgreSQL client
const client = new Client({
  connectionString: `postgresql://postgres.vuoxqclhziyumhrhbsqo:${encodedPassword}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres`,
});

// Function to execute a SQL procedure in PostgreSQL
async function executeProcedure(procedureName) {
  try {
    // Execute the SQL procedure
    await client.query(`CALL ${procedureName}();`);
    console.log(`Execution of ${procedureName} complete.`);
  } catch (err) {
    console.error(`Error executing ${procedureName}:`, err);
  }
}

// Function to run all procedures sequentially
async function runProcedures() {
  try {
    await client.connect(); // Connect to PostgreSQL

    // Execute procedures one by one
    
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily0');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_1');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_2');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily2');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily3');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily4');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily4_1');    
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily5');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_1');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_2');   
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_3');   
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily7');

    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_1_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_2_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily2_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily3_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily4_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily4_1_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily5_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_3_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily7_idefix');
    await executeProcedure('dina_f_akakce_details_fiyatlama_daily7_1_idefix');   

    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_1_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily1_2_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily2_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily3_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily4_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily5_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily6_teknosa');
    //await executeProcedure('dina_f_akakce_details_fiyatlama_daily7_teknosa');
    
    console.log('All procedures executed successfully.');
  } finally {
    await client.end(); // Close the PostgreSQL connection
  }
}

// Run the procedures and catch any errors
runProcedures().catch(err => console.error('Error executing procedures:', err));