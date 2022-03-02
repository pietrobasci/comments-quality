package com.unisannio.ml;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.StringTokenizer;

public class TestArffCreator {

	
	//Crea il file arff con la nuova istanza da classificare
	public static void createTestArff(String path) throws IOException{
		
		Path pathEmpty = Paths.get("ML_file/Empty.arff");
        Path pathTestArff = Paths.get("ML_file/Test.arff");
        Files.copy(pathEmpty, pathTestArff, StandardCopyOption.REPLACE_EXISTING);
        
        BufferedReader br = new BufferedReader(new FileReader(path));
        String instance = "";
        br.readLine();
		int N_features = 0;
        
        while (true){
        	
			String tmp = br.readLine();
			if( tmp == null )
				break;
			StringTokenizer st = new StringTokenizer(tmp);
			
			switch (st.nextToken()){
				case "ANYJ:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;
				case "ANYC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "WPJC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Comments_Density:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "flesch_kincaid_grade:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "flesch_reading_ease:":
					double flesch = Double.parseDouble(st.nextToken());

					if(flesch < 30)
						instance = instance + "Molto-Confusionario" + ",";
					else if (flesch < 50)
						instance = instance + "Difficile" + ",";					
					else if (flesch < 60)
						instance = instance + "Piuttosto-Difficile" + ",";
					else if (flesch < 70)
						instance = instance + "Standard" + ",";
					else if (flesch < 80)
						instance = instance + "Piuttosto-Facile" + ",";
					else if (flesch < 90)
						instance = instance + "Facile" + ",";
					else if (flesch >= 90)
						instance = instance + "Molto-Facile" + ",";
					
					N_features++;					
					break;	
				case "gunning_fog:":
					double fog = Double.parseDouble(st.nextToken());
					
					if (fog < 9)
						instance = instance + "Infantile" + ",";
					else if (fog < 12)
						instance = instance + "Accettabile" + ",";
					else if (fog < 14)
						instance = instance + "Ideale" + ",";
					else if (fog < 18)
						instance = instance + "Difficile" + ",";	
					else if (fog >= 18)
						instance = instance + "Illeggibile" + ",";
					
					N_features++;
					break;
				case "SPW:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Tokens:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Nouns:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Verbs:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;		
				case "RSYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "PSYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "ESYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "DIR:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
			}	
			
		}
		br.close();
        
		instance = instance + "?";
		
		if(N_features == 15) 
			Files.write(pathTestArff, instance.getBytes() , StandardOpenOption.APPEND); 
			  
	}
	
	
	//Crea il training set. Aggiunge i risultati dell'analisi di ogni classe al file TrainingSet_1.arff
	public static void createTrainingArff(String path) throws IOException{
		
        Path pathTrainingArff = Paths.get("ML_file/TrainingSet_1.arff");
		BufferedReader br = new BufferedReader(new FileReader(path));
        String instance = "";
        br.readLine();
		int N_features = 0;
        
        while (true){
        	
			String tmp = br.readLine();
			if( tmp == null )
				break;
			StringTokenizer st = new StringTokenizer(tmp);
			
			switch (st.nextToken()){
				case "ANYJ:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;
				case "ANYC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "WPJC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Comments_Density:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "flesch_kincaid_grade:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "flesch_reading_ease:":
					double flesch = Double.parseDouble(st.nextToken());
					instance = instance + flesch + ",";

					if(flesch < 30)
						instance = instance + "Molto-Confusionario" + ",";
					else if (flesch < 50)
						instance = instance + "Difficile" + ",";					
					else if (flesch < 60)
						instance = instance + "Piuttosto-Difficile" + ",";
					else if (flesch < 70)
						instance = instance + "Standard" + ",";
					else if (flesch < 80)
						instance = instance + "Piuttosto-Facile" + ",";
					else if (flesch < 90)
						instance = instance + "Facile" + ",";
					else if (flesch >= 90)
						instance = instance + "Molto-Facile" + ",";
					
					N_features++;
					break;	
				case "gunning_fog:":
					double fog = Double.parseDouble(st.nextToken());
					instance = instance + fog + ",";
					
					if (fog < 9)
						instance = instance + "Infantile" + ",";
					else if (fog < 12)
						instance = instance + "Accettabile" + ",";
					else if (fog < 14)
						instance = instance + "Ideale" + ",";
					else if (fog < 18)
						instance = instance + "Difficile" + ",";	
					else if (fog >= 18)
						instance = instance + "Illeggibile" + ",";
					
					N_features++;
					break;
				case "SPW:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Tokens:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Nouns:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "Verbs:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;		
				case "RSYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "PSYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "ESYNC:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
				case "DIR:":
					instance = instance + st.nextToken() + ",";
					N_features++;
					break;	
			}	
			
		}
		br.close();
        
		instance = instance + "?\n";
		
		if(N_features == 15)  
			Files.write(pathTrainingArff, instance.getBytes() , StandardOpenOption.APPEND);
		
	}
	
}
