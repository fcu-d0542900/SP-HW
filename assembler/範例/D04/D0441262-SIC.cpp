#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct  Var
{
	char La[10];			//Label
	char VLo[5];			//loc
	Var(){
		memset(this->La,0,sizeof(this->La)); 
		memset(this->VLo,0,sizeof(this->VLo));
	} 
};
struct OgAry
{
	char Location[5];		//計算Object code的 
	struct  Var Op1;		
	char Op2[10];			//Opcode
	char Op3[10];			//Operand
	char Other[50];			//.
	char OBcode[10];		//Object code
	char EndLo[5];	
	OgAry(){
		memset(this->Op2,0,sizeof(this->Op2)); 
		memset(this->Op3,0,sizeof(this->Op3)); 
		memset(this->Other,0,sizeof(this->Other));
		memset(this->OBcode,0,sizeof(this->OBcode));  
		memset(this->Location,0,sizeof(this->Location));
		memset(this->EndLo,0,sizeof(this->EndLo));
	}
};
void Strsplit(const char source[], char dest[], const int start, const int end ); //分割 複製 字串 
int ChangtoX(char ch[],int plus); 		//16->10 + 虛擬
int ChangtoD(char ch);		//16->10 (ABCDEF) 
void CalLocation(OgAry* ); 		//計算Location
void CalOBcode(OgAry* ); 		//計算 OBcode 
void SerLocation(OgAry* );		//label 的 location 

int main(){
	OgAry OA[100];
	char data[10];
	char check[50];
	FILE *fp;
	int i=0;
	int flag=0;
	
	while(flag==0)
	{
		printf("Input your data\n");
		scanf("%s",data);
		fp = fopen(data,"r");
		if(fp!=NULL)
		{
			flag=1;
		}
		else
		{
			printf("File not exist!\n");
		}
	}
	i = 0;
	
	while(fgets(check, sizeof(check), fp))			//分類 Lable Opcode Operand 
	{
		// first char is dot => comment
		if(check[0]=='.')
		{
			strcpy(OA[i].Other,check);  			//把 check 複製到 OA[i].Other 
		}
		else
		{
			char str[50];
			// Check check[0]-check[8]

			memset(str, 0, sizeof(str)); //清空陣列
			Strsplit(check, str, 0, 7);		//分割字串 可以將 check分割的字串存到str中		0->起始位置		7->結束位置 
      		// 檢查是不是空的
			if(str[0]!='\0')
			{
				// 如果不是空的，這邊就是Label
				strcpy(OA[i].Op1.La, str);			//把 str 複製到 OA[i].Op1.La
			}

      		memset(str, 0, sizeof(str)); //清空陣列
			Strsplit(check, str, 7, 15);
			// 檢查是不是空的
			if(str[0]!='\0')
			{
				// 如果不是空的，這邊就是Opcode
				strcpy(OA[i].Op2, str);			//把 str 複製到 OA[i].Op2 
			}

			memset(str, 0, sizeof(str)); //清空陣列
			Strsplit(check, str, 15, 34);
			// 檢查是不是空的
			if(str[0]!='\0')
			{
				// 如果不是空的，這邊就是Operand
				strcpy(OA[i].Op3, str);			//把 str 複製到 OA[i].Op3
			}
		}
		i++;
	}

	//都放到 OA了 

	fclose(fp);
	
	CalLocation(OA); 		
	SerLocation(OA); 		//找到label 的 location 
	CalOBcode(OA);			//計算OBcode 
	//列印 
	printf("----------------------------------------------------\n");
	int c=5; 
	for(i=0;i<100;i++)
	{
		if(OA[i].Other[0]=='\0')
		{
			printf("%3d  %4s %-8s %-5s %-18s ",c,OA[i].Op1.VLo,OA[i].Op1.La, OA[i].Op2, OA[i].Op3); 
			if(OA[i].OBcode[0]!='\0')
			{
				printf("%06s",OA[i].OBcode); 
			}
			printf("\n"); 
		}
		else if(OA[i].Other[0]!='\0')
		{
			printf("%3d  %s",c,OA[i].Other);
		}
		c=c+5;
		if(OA[i].Other[0]=='\0' && OA[i].Op1.VLo[0]=='\0')
		{
			 break; 
		} 
	} 
	printf("----------------------------------------------------\n"); 

	 system("pause");
	return 0;

}
//計算Location 
void CalLocation(OgAry OA[])
{
	int i,temp,Add,tp;
	char temp1[5];  
	 
	for(i=0;i<100;i++)
	{
		if(strcmp(OA[i].Op2,"START")==0)		//strcmp 比較字串 
		{
			strcpy(OA[i].Op1.VLo,OA[i].Op3); 		//複製字串 
			strcpy(OA[i+1].Op1.VLo,OA[i].Op3);
			i=i+1; 
		} 
		else if(OA[i].Op2[0]=='\0' || strcmp(OA[i].Op2,"END")==0) 
		{
			Add=ChangtoX(OA[i-1].Op1.VLo,0); 
			sprintf(OA[i].Op1.VLo,"%X",Add);
		} 
		else if(strcmp(OA[i].Op2,"RESB")==0)
		{
			Add=ChangtoX(OA[i-1].Op1.VLo,3); 
			sprintf(OA[i].Op1.VLo,"%X",Add); 
			temp=atoi(OA[i].Op3); //4096 
			temp=temp+Add; 
			sprintf(temp1,"%X",temp);  	 
		} 
		
		else if(strcmp(OA[i-4].Op2,"RESB")==0)
		{
			strcpy(OA[i].Op1.VLo,temp1); 	 
		} 
		else 
		{ 
			Add=ChangtoX(OA[i-1].Op1.VLo,3); 
			sprintf(OA[i].Op1.VLo,"%X",Add); 
		} 
		if(strcmp(OA[i-1].Op2,"BYTE")==0 && OA[i-1].Op3[0]=='X')
		{	 
			Add=ChangtoX(OA[i-1].Op1.VLo,1); 
			sprintf(OA[i].Op1.VLo,"%X",Add); 
		} 
	}
	for(i=0;i<100;i++)
	{
		if(strcmp(OA[i].Op2,"END")==0)
		{
			strcpy(OA[i].EndLo,OA[i].Op1.VLo);	
			memset(OA[i].Op1.VLo,0,sizeof(OA[i].Op1.VLo));  	
		}
		else if(OA[i].Op2[0]=='\0')
		{ 
			memset(OA[i].Op1.VLo,0,sizeof(OA[i].Op1.VLo));  
		} 
	}  
}  
//label 的 location 
void SerLocation(OgAry OA[])
{
	int i,j;
	for(i=0;i<100;i++)
	{
		for(j=0;j<100;j++) 
		{ 
			if(strcmp( OA[i].Op1.La , OA[j].Op3 ) == 0)		//比較  Label 跟  Operand
			{
				strcpy(OA[j].Location,OA[i].Op1.VLo); 		//strcpy(1,2) 將 2 複製 到 1      label的 location 
			} 
		} 
	}	
}
//計算 OBcode 
void CalOBcode(OgAry OA[])
{
	int i,j,temp;
	int temp1=0; 
	for(i=0;i<100;i++)
	{
		if(strcmp(OA[i].Op2,"STL")==0) 
		{
			strcpy(OA[i].OBcode,"14");  
			strcat(OA[i].OBcode,OA[i].Location);  	//strcat (1,2) 把 2 接到 1  回傳 1 
		} 
		else if(strcmp(OA[i].Op2,"JSUB")==0)
		{
			strcpy(OA[i].OBcode,"48");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"LDA")==0)
		{
			strcpy(OA[i].OBcode,"00");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"COMP")==0)
		{
			strcpy(OA[i].OBcode,"28");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"JEQ")==0)
		{
			strcpy(OA[i].OBcode,"30");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"JS")==0)
		{
			strcpy(OA[i].OBcode,"3C");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"STA")==0)
		{
			strcpy(OA[i].OBcode,"0C");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"LDL")==0)
		{
			strcpy(OA[i].OBcode,"08");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"RESUB")==0)
		{
			strcpy(OA[i].OBcode,"4C");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"LDX")==0)
		{
			strcpy(OA[i].OBcode,"04");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"TD")==0)
		{
			strcpy(OA[i].OBcode,"E0");  
			strcat(OA[i].OBcode,OA[i].Location);  
		}
		else if(strcmp(OA[i].Op2,"RD")==0)
		{
			strcpy(OA[i].OBcode,"D8");  
			strcat(OA[i].OBcode,OA[i].Location);  
		}  
		else if(strcmp(OA[i].Op2,"STCH")==0)
		{
			strcpy(OA[i].OBcode,"54");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"TIX")==0)
		{
			strcpy(OA[i].OBcode,"2C");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"JLT")==0)
		{
			strcpy(OA[i].OBcode,"38");  
			strcat(OA[i].OBcode,OA[i].Location);  
		}
		else if(strcmp(OA[i].Op2,"STX")==0)
		{
			strcpy(OA[i].OBcode,"10");  
			strcat(OA[i].OBcode,OA[i].Location);  
		}  
		else if(strcmp(OA[i].Op2,"LDCH")==0)
		{
			strcpy(OA[i].OBcode,"50");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"WD")==0)
		{
			strcpy(OA[i].OBcode,"DC");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"TIX")==0)
		{
			strcpy(OA[i].OBcode,"2C");  
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"RSUB")==0)//RSUB 
		{
			strcpy(OA[i].OBcode,"4C");  
			strcat(OA[i].OBcode,"0000");  
		} 
		else if(strcmp(OA[i].Op2,"WORD")==0)//WORD
		{
			strcpy(OA[i].OBcode,"00");  
			temp=atoi(OA[i].Op3);
			sprintf(OA[i].Location,"%X",temp);
			strcat(OA[i].OBcode,OA[i].Location);  
		} 
		else if(strcmp(OA[i].Op2,"BYTE")==0)//BYTE
		{
			if(OA[i].Op3[0]=='C')
			{
				strcpy(OA[i].OBcode,"454F46"); 	
			}
			else if(OA[i].Op3[0]=='X')
			{
				if(temp1==0)
				{
					strcpy(OA[i].OBcode,"F1    ");
					temp1=temp+1;
				}
				else
				{
					strcpy(OA[i].OBcode,"05    ");
				}
			}
		} 
	}	
} 	

//分割字元 
void Strsplit(const char source[], char dest[], const int start, const int end ){
	int i = 0, firstChar = 0, lastChar = 0;
	// 檢查第一個跟最後一個非空白字元
	for(i = start;i<end;i++)
	{
		if(source[i]!=' ')
		{
			firstChar = i;
			break;
		}
	}
	for(i = end-1;i>=start;i--)
	{
		if(source[i]!=' ')
		{
			lastChar = i;
			break;
		}
	}

	// 根據檢查結果複製字串
	if(lastChar > firstChar)
	{
		for(i=firstChar;i<=lastChar;i++)
		{
			if(source[i]!='\n' && source[i]!='\0')
			{ 
    		    dest[i-firstChar] = source[i];
    		} 
		}
	}
	dest[i] = '\0';
	return;
}

//16->10 + 虛擬 
int ChangtoX(char ch[],int plus)
{
	int i; 
	int temp[5]; 
	int all;

	for(i=0;i<4;i++)
	{ 
		temp[i]=ChangtoD(ch[i]);
	} 
	temp[0]=temp[0]*16*16*16;
	temp[1]=temp[1]*16*16;
	temp[2]=temp[2]*16; 
	all=temp[0]+temp[1]+temp[2]+temp[3]+plus;
	return all; 
}
//16->10
int ChangtoD(char ch)		
{
	int cg; 
	if(ch=='A')
	{
		cg=10; 
	} 
	else if(ch=='B')
	{
		cg=11; 
	} 
	else if(ch=='C')
	{
		cg=12; 
	}
	else if(ch=='D')
	{
		cg=13; 
	}
	else if(ch=='E')
	{
		cg=14; 
	}
	else if(ch=='F')
	{
		cg=15; 
	} 
	else if(ch=='\0')
	{
		cg=0; 
	} 
	else
	{
		cg=ch-48; 
	}  
	return cg; 
}


