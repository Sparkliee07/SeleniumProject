package Classroom;

import java.util.LinkedHashSet;
import java.util.Set;

public class Interview {
	public static void main(String[] args)
	{
		String companyName = "amazon";
		char[] allchars = companyName.toCharArray();
		Set<Character> unique = new LinkedHashSet<Character>();
		
		for(int i=0;i<allchars.length;i++)
		{
			if(unique.add(allchars[i]))
			{
				System.out.print(allchars[i]);
			}
		}
		
		
	}

}
