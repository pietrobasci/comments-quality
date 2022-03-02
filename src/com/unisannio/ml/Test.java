package com.unisannio.ml;
import java.util.Vector;


public class Test {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		String classifier = "MultilayerPerceptron";
	    //String filter = "weka.filters.unsupervised.instance.Randomize";
	    String dataset = "ML_file/" + "iris.arff";
	    //Per fare previsione su file diverso
	    //String dataset = "iris.txt";
	    Vector<String> classifierOptions = new Vector<String>();
	    //Vector<String> filterOptions = new Vector<String>();

	    //option
	    String opt = "-H";
	    String val = "3,3,3";
	    classifierOptions.add(opt);
	    classifierOptions.add(val);
	    
	    WekaDemo demo = new WekaDemo();
	    demo.setClassifier(classifier, classifierOptions.toArray(new String[classifierOptions.size()]));
	    //demo.setFilter(filter, filterOptions.toArray(new String[filterOptions.size()]));
	    demo.setTraining(dataset);
	    //per addestrare modello (solo la prima volta)
	    demo.execute(false);
	    //per stampare caratteristiche modello
	    System.out.println(demo.toString());
	    demo.doPrediction("ML_file/Test.arff");

	}

}
