package com.unisannio.controller;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Vector;

import com.unisannio.ml.TestArffCreator;
import com.unisannio.ml.WekaDemo;


public class AnalysisControl {

	private String parentPath, pkg;
	private WekaDemo model;
	private String classifier, dataset;
	//private String filter;
    Vector<String> classifierOptions = new Vector<String>();
    Vector<String> filterOptions = new Vector<String>();
	
    
    
	public AnalysisControl() throws Exception {
		
		super();
		model = new WekaDemo();
		classifier = "J48";
	    //filter = "weka.filters.unsupervised.instance.Randomize";
	    dataset = "ML_file/" + "TrainingSet.arff";	    
	    
	    model.setClassifier(classifier, classifierOptions.toArray(new String[classifierOptions.size()]));
	    //demo.setFilter(filter, filterOptions.toArray(new String[filterOptions.size()]));
	    model.setTraining(dataset);
	    //per training modello (solo la prima volta)
	    model.execute(false);
	   
	}
	
	
	public double analizePackage(String path) throws Exception {
		
		Path uri = Paths.get(path);
		parentPath = uri.getParent().toString() + "/";
		pkg = uri.getFileName().toString();
		
		String script1 = "script/ExtractComments.py";
		Process p = Runtime.getRuntime().exec("python" + " " + script1 + " " + parentPath + " " + pkg);
		p.waitFor();
		
		String script2 = "script/Consistency_1.py";
	    Process p1 = Runtime.getRuntime().exec("python" + " " + script2 + " " + parentPath + " " + pkg);
		p1.waitFor();
		
		String script3 = "script/Readability.py";
		Process p2 = Runtime.getRuntime().exec("python" + " " + script3 + " " + pkg);
		p2.waitFor();
		
		String script4 = "script/Understandability.py";
		Process p3 = Runtime.getRuntime().exec("python" + " " + script4 + " " + pkg);
		p3.waitFor();
		
		String script5 = "script/Consistency_2.py";
		Process p4 = Runtime.getRuntime().exec("python" + " " + script5 + " " + pkg);
		p4.waitFor();
		
		
		TestArffCreator.createTestArff("file/metriche/Metriche_" + pkg + ".txt");

		return model.doPrediction("ML_file/Test.arff");
	
	}
	
	public double analizeProject(String path) throws Exception {
		
		Path uri = Paths.get(path);
		parentPath = uri.getParent().toString() + "/";
		pkg = uri.getFileName().toString();

		String script1 = "script/ExtractComments.py";
		Process p = Runtime.getRuntime().exec("python" + " " + script1 + " " + parentPath + " " + pkg);
		p.waitFor();
		
		String script2 = "script/Consistency_1.py";
	    Process p1 = Runtime.getRuntime().exec("python" + " " + script2 + " " + parentPath + " " + pkg);
		p1.waitFor();
		
		String script3 = "script/Readability.py";
		Process p2 = Runtime.getRuntime().exec("python" + " " + script3 + " " + pkg);
		p2.waitFor();
		
		String script4 = "script/Understandability.py";
		Process p3 = Runtime.getRuntime().exec("python" + " " + script4 + " " + pkg);
		p3.waitFor();
		
		String script5 = "script/Consistency_2.py";
		Process p4 = Runtime.getRuntime().exec("python" + " " + script5 + " " + pkg);
		p4.waitFor();
		
		
		TestArffCreator.createTestArff("file/metriche/Metriche_" + pkg + ".txt");
           
		return model.doPrediction("ML_file/Test.arff");
		
	}
	
	public double analizeClass(String path) throws Exception {
        
		new File("file/tmpPKG").mkdirs();
        
        Path pathSource = Paths.get(path);
        Path pathTarget = Paths.get("file/tmpPKG/ClassToAnalyze.java");
        Files.copy(pathSource, pathTarget, StandardCopyOption.REPLACE_EXISTING);
        
        Path uri = pathTarget.toAbsolutePath().getParent();
		parentPath = uri.getParent().toString() + "/";
		pkg = uri.getFileName().toString();

		String script1 = "script/ExtractComments.py";
		Process p = Runtime.getRuntime().exec("python" + " " + script1 + " " + parentPath + " " + pkg);
		p.waitFor();
		
		String script2 = "script/Consistency_1.py";
	    Process p1 = Runtime.getRuntime().exec("python" + " " + script2 + " " + parentPath + " " + pkg);
		p1.waitFor();
		
		String script3 = "script/Readability.py";
		Process p2 = Runtime.getRuntime().exec("python" + " " + script3 + " " + pkg);
		p2.waitFor();
		
		String script4 = "script/Understandability.py";
		Process p3 = Runtime.getRuntime().exec("python" + " " + script4 + " " + pkg);
		p3.waitFor();
		
		String script5 = "script/Consistency_2.py";
		Process p4 = Runtime.getRuntime().exec("python" + " " + script5 + " " + pkg);
		p4.waitFor();
		
		
		
		BufferedReader stdInput = new BufferedReader(new InputStreamReader(p1.getInputStream()));

		BufferedReader stdError = new BufferedReader(new InputStreamReader(p1.getErrorStream()));
		
           // read the output from the command
           System.out.println("Here is the standard output of the command:\n");
           String s=null;
           while ((s = stdInput.readLine()) != null) {
               System.out.println(s);
           }
           
           // read any errors from the attempted command
           System.out.println("Here is the standard error of the command (if any):\n");
           while ((s = stdError.readLine()) != null) {
               System.out.println(s);
           }
           
         
           
		
		TestArffCreator.createTestArff("file/metriche/Metriche_" + pkg + ".txt");
		
		//Usato per creare il file TrainingSet_1.arff
		TestArffCreator.createTrainingArff("file/metriche/Metriche_" + pkg + ".txt");

		
		return model.doPrediction("ML_file/Test.arff");
		
	}

	public void setModel(String classifier, Vector<String> classifierOptions, String dataset) throws Exception{
		
		model = new WekaDemo();
		this.classifier = classifier;
	    //filter = "weka.filters.unsupervised.instance.Randomize";
	    this.dataset = dataset;	    
	    
	    model.setClassifier(classifier, classifierOptions.toArray(new String[classifierOptions.size()]));
	    //demo.setFilter(filter, filterOptions.toArray(new String[filterOptions.size()]));
	    model.setTraining(dataset);
	    model.execute(true);
	    
	}
	
	public String getModelInfo(){
		
		return model.toString();
		
	}
	
	public String getMetrics() throws IOException{
		
		BufferedReader br = new BufferedReader(new FileReader("file/metriche/Metriche_" + pkg + ".txt"));
		String metrics = "";
		
		while (true){
			String tmp = br.readLine();
			if( tmp == null )
				break;
			metrics = metrics + tmp + "\n";
		}
		br.close();
		
		return metrics;
		
	}
	
}
