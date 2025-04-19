package JavaAdvanceOOPS;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Learnlist {
	public static void main(String[] args)
	{
		
//		List(Dynamic array)
//		List -> Interface -:> you canot creat a object
//		Hold data that can grow and shrink
//		It allows to hold dublicate data
//		Implementation class -> ArrayList(index),Linked List(next,prev)
//
//		Methods//
//		Sze add, remove,get contins
//		Generic// store the type of allowed data on the given data structure
//		List<String> learners = new ArrayList <String>();
//		List is a interface arraylist is the implementation class of interface
//		Learners.add("rmaon");
		
		List<String> books = new ArrayList<String>();
		books.add("5 AM Clock");
		books.add("Muganimbikai");
		System.out.println(books);
		System.out.println(books.size());
		books.add(0,"power of bow");
		System.out.println(books);
		books.get(books.size()-1);
		System.out.println(books);
		books.contains("Mugambikia");
		System.out.println(books.contains("Mugambikia"));
		
		Collections.sort(books); //Collections is a class 
//		Collections.reverse(books);
		System.out.println(books);
		for(int i=0;i<books.size();i++)
		{
			System.out.println(books.get(i));
			
		}
	}

}
