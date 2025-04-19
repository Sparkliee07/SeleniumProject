package JavaAdvanceOOPS;

import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.TreeSet;

public class LearnSet {

	public static void main(String[] args) {
		 
		// Set -> Dynamic Array
		 
		// Set -> Interface -> You cannot create an object
		 
		// Hold data that can grow or shrink !!
		 
		// It allows to hold unique data (No duplicates allowed)
		 
		// Implementation class > HashSet, LinkedHashSet, TreeSet
		 
		/* 
		* HashSet -> Hashing algorithm (Java internally create hashing value for each key)
		* LinkedHashSet -> Maintains the order of adding (like List)
		* TreeSet -> Uses Comparator -> ASCII value
		// Methods
		 
		/*
		* size -> how many items are there in the list -> int
		* add -> add a new item to the list (by default it will add to the last->int
		* remove -> remove given index or data from the list (if there are multiple, removes first) 
		* contains -> find whether given item is present or not -> boolean 
		* 
		* No get method for the Set !! 
		* 
		*/
		 
		// Generic -> Stores the type of allowed data in the given data structure
        Set<String> companies = new HashSet<String>();//Hashing algorthim add
        companies.add("Syntel");
        companies.add("Hcl");
        companies.add("Tcs");
        companies.add("Hcl");
        boolean add1=companies.add("Hcl");//Won't allow duplicates
        System.out.println(add1);
        
        System.out.println(companies);
        
        Set<String> companies2 = new LinkedHashSet<String>();
        companies2.add("Syntel");
        companies2.add("Hcl");
        companies2.add("Tcs");
        companies2.add("Hcl");
        boolean add2=companies2.add("Hcl");//Won't allow duplicates
        System.out.println(add2);
        
        System.out.println(companies2);
        Set<String> companies1 = new TreeSet<String>(); // follow lst order
        companies1.add("Syntel");
        companies1.add("Hcl");
        companies1.add("Tcs");
        companies1.add("Hcl");
        boolean ad2=companies1.add("Hcl");//Won't allow duplicates
        System.out.println(ad2);
        
        System.out.println(companies1);
	}
	
}
