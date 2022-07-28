#include "Texture.h"
#include "stb_image\stb_image.h"
Texture::Texture(const std::string& path)
	:m_RendererID(0), m_FilePath(path), m_localBuffer(nullptr), m_Width(0), m_Height(0), m_BPP(0)
{
	stbi_set_flip_vertically_on_load(1); // should be flipped because the opengl pixels start from bottom left rather than top left
	m_localBuffer = stbi_load(path.c_str(), &m_Width, &m_Height, &m_BPP, 4); // 4 -- how many desired channels we need in this case RGBA so 4

	GLCall(glGenTextures(1, &m_RendererID));
	GLCall(glBindTexture(GL_TEXTURE_2D, m_RendererID));

	/*We need to specify the following 4 parameters in order to work or we get a black screen*/
	GLCall(glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER/*minimazation filter*/, GL_LINEAR)); //To linearly sample everything
	GLCall(glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER/*magnification filter -- larger in the pixels than the actual pixel size and we need to scale it up*/, GL_LINEAR));
	GLCall(glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)); //When we don't want to extend the area
	GLCall(glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)); //When we don't want to extend the area
	
	GLCall(glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, m_Width, m_Height, 0, GL_RGBA, GL_UNSIGNED_BYTE, m_localBuffer));
	GLCall(glBindTexture(GL_TEXTURE_2D, 0));

	if (m_localBuffer)
		stbi_image_free(m_localBuffer);
	printf("%s", stbi_failure_reason());
}

Texture::~Texture()
{
	GLCall(glDeleteTextures(1, &m_RendererID));
}

void Texture::Bind(unsigned int slot) const
{
	GLCall(glActiveTexture(GL_TEXTURE0 + slot));
	GLCall(glBindTexture(GL_TEXTURE_2D, m_RendererID));
}

void Texture::Unbind() const
{
	GLCall(glBindTexture(GL_TEXTURE_2D, 0));
}

