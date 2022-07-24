#pragma once
#include <vector>
#include "Renderer.h"
#include "GL/glew.h"

struct VertexBufferElement
{
	
	unsigned int type; 
	unsigned int count;
	unsigned char normalized;

	static unsigned int GetSizeOfType(unsigned int type)
	{
		switch (type)
		{
		case GL_FLOAT: return 4;
		case GL_UNSIGNED_INT: return 4;
		case GL_UNSIGNED_BYTE: return 1;
		}
		ASSERT(false);
		return 0;
	}
};

class VertexBufferLayout
{
private:
	std::vector<VertexBufferElement> m_Elements;
	unsigned int m_Stride;
public:
	VertexBufferLayout()
		:m_Stride(0){}
	template <typename T>
	void Push(int count)
	{
		//static_assert(false);
	}
	template <>
	void Push<float>(int count)
	{
		VertexBufferElement tempa = { GL_FLOAT, (unsigned int)count, false };
		m_Elements.push_back(tempa);
		m_Stride += count*VertexBufferElement::GetSizeOfType(GL_FLOAT);
	}
	template <>
	void Push<unsigned int>(int count)
	{
		VertexBufferElement tempb = { GL_UNSIGNED_INT,(unsigned int)count, false };
		m_Elements.push_back(tempb);
		m_Stride += count*VertexBufferElement::GetSizeOfType(GL_UNSIGNED_INT);
	}
	template <>
	void Push<unsigned char>(int count)
	{
		VertexBufferElement tempc = { GL_UNSIGNED_BYTE,(unsigned int)count, true };
		m_Elements.push_back(tempc);
		m_Stride += count*VertexBufferElement::GetSizeOfType(GL_UNSIGNED_BYTE);
	}

	inline const std::vector<VertexBufferElement> GetElements() const { return m_Elements; }
	inline unsigned int GetStride() const { return m_Stride; }
};

